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


class Price(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="prices"
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
