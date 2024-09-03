from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from shop.models import Category
from shop.serializers import ProductSerializer
from shop.shop_settings import Category_ICON_MAX_SIZE as size_limit


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the `Category` model used for read operations.

    This serializer includes fields for category details such as name, slug,
    icon, and associated products. It also handles validation for the icon file
    size.
    """

    icon = serializers.ImageField(required=False, allow_null=True)
    isActive = serializers.BooleanField(source="is_active", default=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "icon",
            "isActive",
            "createdAt",
            "updatedAt",
            "products",
        ]
        read_only_fields = ["id", "updatedAt", "createdAt", "products"]

    def validate_icon(self, value):
        """
        Validate the size of the uploaded icon image.

        Checks if the size of the uploaded icon exceeds the maximum allowed size
        defined in the settings. If it does, a validation error is raised.

        Args:
            value: The uploaded image file.

        Returns:
            The validated image file.

        Raises:
            serializers.ValidationError: If the image file is larger than the allowed size.
        """
        if value:
            if value.size > size_limit:
                raise serializers.ValidationError(
                    _(
                        f"Image file is too large (more than {size_limit / 1024 / 1024} MB) !"
                    )
                )
        return value


class CategoryUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating the `Category` model.

    This serializer includes fields for category details such as name, slug,
    and icon, but does not include associated products. It also handles validation
    for the icon file size.
    """

    icon = serializers.ImageField(required=False, allow_null=True)
    isActive = serializers.BooleanField(source="is_active", default=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "icon",
            "isActive",
            "createdAt",
            "updatedAt",
        ]
        read_only_fields = ["id", "updatedAt", "createdAt"]

    def validate_icon(self, value):
        """
        Validate the size of the uploaded icon image for updates.

        Checks if the size of the uploaded icon exceeds the maximum allowed size
        defined in the settings. If it does, a validation error is raised.

        Args:
            value: The uploaded image file.

        Returns:
            The validated image file.

        Raises:
            serializers.ValidationError: If the image file is larger than the allowed size.
        """
        if value:
            if value.size > size_limit:
                raise serializers.ValidationError(
                    _(
                        f"Image file is too large (more than {size_limit / 1024 / 1024} MB) !"
                    )
                )
        return value
