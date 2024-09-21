from django.contrib import admin
from django.utils.html import format_html
from menu.models import Category, Product


class ProductInline(admin.TabularInline):
    """
    Inline admin interface for `Product` model within the `Category` admin.

    This class configures how `Product` instances are displayed within the
    `Category` admin form. It includes fields for name, slug, and activity status,
    and allows editing of the creation and update timestamps.
    """

    model = Product
    extra = 1  # Number of empty forms to display
    readonly_fields = ("created_at", "updated_at")
    fields = ("name", "slug", "is_active", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("name",)}
    can_delete = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for `Category` model.

    This class configures the admin interface for `Category` with options for
    displaying, searching, filtering, and editing categories. It also includes
    actions to activate or deactivate selected categories.
    """

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
        """
        Display a thumbnail of the category icon in the admin list view.

        If an icon is available for the category, it renders as an HTML image tag.
        Otherwise, returns an empty string.

        Args:
            obj: The category instance being rendered.

        Returns:
            str: HTML markup for displaying the category icon.
        """
        if obj.icon:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius:12%;" />',
                obj.icon.url,
            )
        return ""

    icon_display.short_description = "Icon"

    actions = ["make_active", "make_inactive"]

    def make_active(self, request, queryset):
        """
        Mark selected categories as active.

        This action updates the `is_active` field of the selected categories to
        `True` and provides a success message.

        Args:
            request: The HTTP request object.
            queryset: The queryset of selected categories.

        Returns:
            None
        """
        updated = queryset.update(is_active=True)
        self.message_user(request, f"Successfully activated {updated} categories.")

    make_active.short_description = "Activate selected categories"

    def make_inactive(self, request, queryset):
        """
        Mark selected categories as inactive.

        This action updates the `is_active` field of the selected categories to
        `False` and provides a success message.

        Args:
            request: The HTTP request object.
            queryset: The queryset of selected categories.

        Returns:
            None
        """
        updated = queryset.update(is_active=False)
        self.message_user(request, f"Successfully deactivated {updated} categories.")

    make_inactive.short_description = "Deactivate selected categories"
