from rest_framework import serializers
from menu.models import Category, Product


class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer for `Category` model to represent a category in the menu.
    """

    icon = serializers.ImageField(read_only=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "icon",
            "createdAt",
            "updatedAt",
        ]
        read_only_fields = [
            "id",
            "name",
            "slug",
            "icon",
            "createdAt",
            "updatedAt",
        ]


class MenuProductSerializer(serializers.ModelSerializer):
    """
    Serializer for `Product` model to represent a product within a category in the menu.
    """

    price = serializers.SerializerMethodField(read_only=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "price",
            "updatedAt",
            "createdAt",
        ]
        read_only_fields = [
            "id",
            "name",
            "slug",
            "price",
            "updatedAt",
            "createdAt",
        ]

    def get_price(self, obj):
        """
        Returns the most recent active price for the given product.
        """
        return (
            obj.most_recent_active_price
            if obj.most_recent_active_price is not None
            else 0
        )


class MenuDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for `Category` model that includes detailed information about the category
    and its associated products.
    """

    products = MenuProductSerializer(many=True, read_only=True)
    icon = serializers.ImageField(required=False, allow_null=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "icon",
            "products",
            "createdAt",
            "updatedAt",
        ]
        read_only_fields = [
            "id",
            "name",
            "slug",
            "icon",
            "products",
            "createdAt",
            "updatedAt",
        ]
