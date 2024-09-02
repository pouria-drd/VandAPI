from django.contrib import admin
from shop.models import Product, Price
from django.utils.html import format_html


class PriceInline(admin.TabularInline):
    model = Price
    extra = 1  # Number of empty forms to display
    readonly_fields = ("created_at", "updated_at")
    fields = ("amount", "is_active", "created_at", "updated_at")
    can_delete = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [PriceInline]
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        "name",
        "slug",
        "category",
        # "price_display",
        "is_active",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)
    search_fields = ("name", "slug")
    list_filter = ("is_active", "category")

    def price_display(self, obj):
        """Display the main price for the product."""
        price = obj.price
        return format_html(
            '<span style="color: #059669;">${}</span>',
            price,
        )

    price_display.short_description = "Final Price"
