from shop.models import Product
from rest_framework import serializers
from shop.serializers import PriceSerializer


class ProductSerializer(serializers.ModelSerializer):
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
