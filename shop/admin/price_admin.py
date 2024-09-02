from shop.models import Price
from django.contrib import admin
from django.utils.html import format_html


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
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
        if obj:  # Editing an existing object
            return self.readonly_fields + ("product",)
        return self.readonly_fields

    def activate_prices(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"Successfully activated {updated} prices.")

    activate_prices.short_description = "Activate selected prices"

    def deactivate_prices(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"Successfully deactivated {updated} prices.")

    deactivate_prices.short_description = "Deactivate selected prices"
