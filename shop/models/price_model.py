import uuid
from django.db import models
from .product_model import Product
from django.utils.translation import gettext_lazy as _


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
            models.Index(fields=["product", "is_active", "created_at"]),
        ]

    def __str__(self):
        return f"{self.product.name} - {str(self.amount)}"
