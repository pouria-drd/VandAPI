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
            "category",
            "isActive",
            "updatedAt",
            "createdAt",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    prices = serializers.SerializerMethodField()
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
            "prices",
        ]

    def get_prices(self, obj):
        prices = obj.prices.all()
        return PriceSerializer(prices, many=True).data
