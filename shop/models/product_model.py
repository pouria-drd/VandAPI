import uuid
from django.db import models
from .category_model import Category
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, related_name="products"
    )

    name = models.CharField(_("name"), max_length=60)
    slug = models.SlugField(_("slug"), max_length=60, unique=True)

    is_active = models.BooleanField(_("is active"), default=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"

        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name", "slug", "is_active"]),
        ]

    def __str__(self):
        return self.name


class Discount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(_("name"), max_length=100)
    description = models.TextField(_("description"), blank=True, null=True)

    discount_percentage = models.DecimalField(
        _("discount percentage"), max_digits=5, decimal_places=2
    )

    is_active = models.BooleanField(_("is active"), default=True)
    start_date = models.DateTimeField(_("start date"), null=True, blank=True)
    end_date = models.DateTimeField(_("end date"), null=True, blank=True)

    def __str__(self):
        return self.name + " - " + self.discount_percentage


class Price(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="prices"
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        related_name="prices",
        null=True,
        blank=True,
    )

    amount = models.DecimalField(_("amount"), max_digits=10, decimal_places=2)

    is_active = models.BooleanField(_("is active"), default=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        verbose_name = "price"
        verbose_name_plural = "prices"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["amount", "is_active", "created_at"]),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.amount}"

    def get_final_price(self):
        """Returns the final price after applying the linked discount."""
        if self.discount and self.discount.is_active:
            discount_amount = self.amount * (self.discount.discount_percentage / 100)
            return self.amount - discount_amount

        return self.amount
