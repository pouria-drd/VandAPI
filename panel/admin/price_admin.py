from panel.models import Price
from django.contrib import admin


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    """
    Admin interface for `Price` model.

    This class configures the admin interface for `Price` with options for
    displaying, searching, filtering, and editing prices. It includes actions
    to activate or deactivate selected prices.
    """

    list_display = [
        "product",
        "amount",
        "is_active",
        "created_at",
        "updated_at",
    ]

    ordering = ("-created_at",)
    list_filter = ("is_active", "amount")
    search_fields = ("product__name", "amount")
    readonly_fields = ("created_at", "updated_at")

    actions = [
        "activate_prices",
        "deactivate_prices",
    ]

    def get_readonly_fields(self, request, obj=None):
        """
        Return the readonly fields for the `Price` admin form.

        This method ensures that the `product` field is readonly when editing an
        existing price instance.

        Args:
            request: The HTTP request object.
            obj: The `Price` instance being edited (if any).

        Returns:
            tuple: Tuple of readonly field names.
        """
        if obj:  # Editing an existing object
            return self.readonly_fields + ("product",)
        return self.readonly_fields

    def activate_prices(self, request, queryset):
        """
        Mark selected prices as active.

        This action updates the `is_active` field of the selected prices to
        `True` and provides a success message.

        Args:
            request: The HTTP request object.
            queryset: The queryset of selected prices.

        Returns:
            None
        """
        updated = queryset.update(is_active=True)
        self.message_user(request, f"Successfully activated {updated} prices.")

    activate_prices.short_description = "Activate selected prices"

    def deactivate_prices(self, request, queryset):
        """
        Mark selected prices as inactive.

        This action updates the `is_active` field of the selected prices to
        `False` and provides a success message.

        Args:
            request: The HTTP request object.
            queryset: The queryset of selected prices.

        Returns:
            None
        """
        updated = queryset.update(is_active=False)
        self.message_user(request, f"Successfully deactivated {updated} prices.")

    deactivate_prices.short_description = "Deactivate selected prices"
