import os
import uuid
from PIL import Image
from dotenv import load_dotenv

from django.db import models
from django_cleanup import cleanup
from django.dispatch import receiver
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from panel.panel_settings import Category_ICON_MAX_SIZE as size_limit

load_dotenv()  # Loads the variables from the .env file into the environment


# Load allowed extensions from environment variable
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS", "png,jpg,jpeg").split(",")


def category_icon_upload_to(instance, filename):
    """Generate a unique upload path for category icons."""
    return f"category_icons/{instance.id}/{filename}"


@cleanup.select
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(_("name"), max_length=60)
    slug = models.SlugField(_("slug"), max_length=60, unique=True)
    icon = models.ImageField(_("icon"), upload_to=category_icon_upload_to, blank=True)

    is_active = models.BooleanField(_("is active"), default=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        indexes = [
            models.Index(fields=["name", "slug", "is_active"]),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()

        if self.icon:
            # Validate the image file type and size
            ext = self.icon.name.split(".")[-1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                raise ValidationError(
                    _(
                        "Unsupported file extension. Supported extensions are: jpg, jpeg, png!"
                    )
                )
            if self.icon.size > size_limit:
                raise ValidationError(
                    _(
                        f"Image file is too large (more than {size_limit / 1024 / 1024} MB) !"
                    )
                )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


@receiver(models.signals.post_save, sender=Category)
def resize_icon(sender, instance, **kwargs):
    """Resize the icon image if it's larger than 512x512 pixels."""
    if instance.icon:
        img = Image.open(instance.icon.path)
        if img.width > 512 or img.height > 512:
            img.thumbnail((512, 512))
            img.save(instance.icon.path)
