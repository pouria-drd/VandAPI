from panel.models import Product
from rest_framework import serializers
from panel.serializers import PriceSerializer


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Product` model used for read operations.

    This serializer includes fields for product details such as name, slug, price,
    and associated prices. It also includes fields for the active status and timestamps.
    The `price` field represents the most recent price for the product and is read-only.
    """

    prices = PriceSerializer(many=True, read_only=True)
    isActive = serializers.BooleanField(source="is_active", default=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="most_recent_price", read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "price",
            "category",
            "isActive",
            "updatedAt",
            "createdAt",
            "prices",
        ]
        read_only_fields = [
            "id",
            "price",
            "updatedAt",
            "createdAt",
            "prices",
        ]


class ProductUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating the `Product` model.

    This serializer includes fields for product details like name, slug, and category.
    It also includes fields for active status and timestamps but does not include
    information about prices.
    """

    isActive = serializers.BooleanField(source="is_active", default=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "isActive",
            "updatedAt",
            "createdAt",
        ]
        read_only_fields = [
            "id",
            "updatedAt",
            "createdAt",
        ]
