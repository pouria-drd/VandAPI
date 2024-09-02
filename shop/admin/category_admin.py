from django.contrib import admin
from django.utils.html import format_html
from shop.models import Category, Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1  # Number of empty forms to display
    readonly_fields = ("created_at", "updated_at")
    fields = ("name", "slug", "is_active", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("name",)}
    can_delete = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

    list_display = (
        "name",
        "slug",
        "is_active",
        "created_at",
        "updated_at",
        "icon_display",
    )

    search_fields = ("name", "slug")
    list_filter = ("is_active", "created_at", "updated_at")
    readonly_fields = ["created_at", "updated_at"]
    inlines = [ProductInline]

    def icon_display(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius:12%;" />',
                obj.icon.url,
            )
        return ""

    icon_display.short_description = "Icon"

    actions = ["make_active", "make_inactive"]

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"Successfully activated {updated} categories.")

    make_active.short_description = "Activate selected categories"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"Successfully deactivated {updated} categories.")

    make_inactive.short_description = "Deactivate selected categories"
