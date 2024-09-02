from django.contrib import admin
from shop.models import Product, Price


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
        updated = queryset.update(is_active=True)
        self.message_user(request, f"Successfully activated {updated} products.")

    activate_products.short_description = "Activate selected products"

    def deactivate_products(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"Successfully deactivated {updated} products.")

    deactivate_products.short_description = "Deactivate selected products"
