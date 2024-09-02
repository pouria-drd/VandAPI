from shop.models import Product
from rest_framework import serializers
from shop.serializers import PriceSerializer


class ProductSerializer(serializers.ModelSerializer):
    isActive = serializers.BooleanField(source="is_active", default=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

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
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    priceHistory = PriceSerializer(many=True, read_only=True)
    isActive = serializers.BooleanField(source="is_active", default=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

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
            "priceHistory",
        ]
