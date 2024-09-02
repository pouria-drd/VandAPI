from rest_framework import serializers
from shop.models import Product, Price


class PriceSerializer(serializers.ModelSerializer):
    isActive = serializers.BooleanField(source="is_active", default=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Price
        fields = ["id", "amount", "is_active", "created_at", "updated_at"]


class ProductSerializer(serializers.ModelSerializer):
    prices = PriceSerializer(many=True, read_only=True)

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
            "is_active",
            "created_at",
            "updated_at",
            "prices",
        ]
