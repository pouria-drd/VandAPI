from rest_framework import serializers
from shop.models import Product, Discount, Price


class DiscountSerializer(serializers.ModelSerializer):
    discountPercentage = serializers.DecimalField(
        source="discount_percentage", max_digits=5, decimal_places=2
    )
    endDate = serializers.DateTimeField(source="end_date")
    startDate = serializers.DateTimeField(source="start_date")
    isActive = serializers.BooleanField(source="is_active", default=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Discount
        fields = [
            "id",
            "name",
            "description",
            "discountPercentage",
            "createdAt",
            "updatedAt",
            "isActive",
            "startDate",
            "endDate",
        ]


class PriceSerializer(serializers.ModelSerializer):
    discount = DiscountSerializer(
        read_only=True
    )  # Nested serializer for the Discount model
    finalPrice = (
        serializers.SerializerMethodField()
    )  # Custom field to show the final price after discount
    isActive = serializers.BooleanField(source="is_active", default=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Price
        fields = [
            "id",
            "product",
            "amount",
            "discount",
            "finalPrice",
            "isActive",
            "createdAt",
            "updatedAt",
        ]

    def get_finalPrice(self, obj):
        """Calculates the final price after applying the discount."""
        if obj.discount and obj.discount.active:
            discount_amount = obj.amount * (obj.discount.discount_percentage / 100)
            return obj.amount - discount_amount
        return obj.amount


class ProductSerializer(serializers.ModelSerializer):
    prices = PriceSerializer(many=True, read_only=True)
    mainPrice = serializers.SerializerMethodField()
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
            "createdAt",
            "updatedAt",
            "prices",
            "mainPrice",
        ]

    def get_main_price(self, obj):
        """Return the main price for the product."""
        main_price = obj.get_main_price()
        if main_price:
            return PriceSerializer(main_price).data
        return None
