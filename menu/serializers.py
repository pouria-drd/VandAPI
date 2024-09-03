from rest_framework import serializers
from shop.models import Category, Product


class MenuSerializer(serializers.ModelSerializer):
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
    isActive = serializers.BooleanField(source="is_active", default=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)
    price = serializers.SerializerMethodField(read_only=True)

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

        read_only_fields = [
            "id",
            "name",
            "slug",
            "price",
            "category",
            "isActive",
            "updatedAt",
            "createdAt",
        ]

    def get_price(self, obj):
        # Return the annotated price for the active product
        return (
            obj.most_recent_active_price
            if obj.most_recent_active_price is not None
            else 0
        )


class MenuDetailSerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(required=False, allow_null=True)
    isActive = serializers.BooleanField(source="is_active", default=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    products = MenuProductSerializer(many=True, read_only=True)

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
