from django.contrib import admin
from menu.models import Product, Price


class PriceInline(admin.TabularInline):
    """
    Inline admin interface for `Price` model within the `Product` admin.

    This class configures how `Price` instances are displayed within the
    `Product` admin form. It includes fields for amount and activity status,
    and allows editing of the creation and update timestamps.
    """

    model = Price
    extra = 1  # Number of empty forms to display
    readonly_fields = ("created_at", "updated_at")
    fields = ("amount", "is_active", "created_at", "updated_at")
    can_delete = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for `Product` model.

    This class configures the admin interface for `Product` with options for
    displaying, searching, filtering, and editing products. It includes an
    inline interface for managing associated prices and actions to activate
    or deactivate selected products.
    """

    inlines = [PriceInline]
    prepopulated_fields = {"slug": ("name",)}

    list_display = (
        "name",
        "slug",
        "category",
        "is_active",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)
    search_fields = ("name", "slug")
    list_filter = ("is_active", "category")

    actions = [
        "activate_products",
        "deactivate_products",
    ]

    def activate_products(self, request, queryset):
        """
        Mark selected products as active.

        This action updates the `is_active` field of the selected products to
        `True` and provides a success message.

        Args:
            request: The HTTP request object.
            queryset: The queryset of selected products.

        Returns:
            None
        """
        updated = queryset.update(is_active=True)
        self.message_user(request, f"Successfully activated {updated} products.")

    activate_products.short_description = "Activate selected products"

    def deactivate_products(self, request, queryset):
        """
        Mark selected products as inactive.

        This action updates the `is_active` field of the selected products to
        `False` and provides a success message.

        Args:
            request: The HTTP request object.
            queryset: The queryset of selected products.

        Returns:
            None
        """
        updated = queryset.update(is_active=False)
        self.message_user(request, f"Successfully deactivated {updated} products.")

    deactivate_products.short_description = "Deactivate selected products"
