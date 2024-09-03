from rest_framework import serializers
from shop.models import Category, Product, Price


class MenuCategorySerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(read_only=True)
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

        read_only_fields = [
            "id",
            "name",
            "slug",
            "icon",
            "isActive",
            "createdAt",
            "updatedAt",
        ]


class MenuProductSerializer(serializers.ModelSerializer):
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
            "createdAt",
            "updatedAt",
        ]

        read_only_fields = [
            "id",
            "name",
            "slug",
            "price",
            "createdAt",
            "updatedAt",
        ]

    def get_price(self, obj):
        price = obj.prices.filter(is_active=True).order_by("-created_at").first()
        return price.amount if price else 0


class MenuCategoryDetailSerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(required=False, allow_null=True)
    isActive = serializers.BooleanField(source="is_active", default=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    products = serializers.SerializerMethodField()

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

        read_only_fields = [
            "id",
            "name",
            "slug",
            "icon",
            "isActive",
            "createdAt",
            "updatedAt",
            "products",
        ]

    def get_products(self, obj):
        # Filter the products to only include active ones
        active_products = obj.products.filter(is_active=True)
        return MenuProductSerializer(active_products, many=True).data
