from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from shop.models import Category
from shop.shop_settings import Category_ICON_MAX_SIZE as size_limit


class CategorySerializer(serializers.ModelSerializer):
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
        if value:
            if value.size > size_limit:
                raise serializers.ValidationError(
                    _(
                        f"Image file is too large (more than {size_limit / 1024 / 1024} MB) !"
                    )
                )

            return value
