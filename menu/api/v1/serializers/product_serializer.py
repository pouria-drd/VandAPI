from rest_framework import serializers
from menu.models import Product, Price
from .price_serializer import PriceSerializer


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Product` model used for list and create operations.
    """

    isActive = serializers.BooleanField(source="is_active", read_only=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)
    price = serializers.DecimalField(
        source="most_recent_active_price",
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )
    categoryName = serializers.CharField(source="category.name", read_only=True)

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
            "categoryName",
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
            "categoryName",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Product` model used for read operations.

    This serializer includes fields for product details such as name, slug, price,
    and associated prices.
    """

    prices = PriceSerializer(many=True, read_only=True)
    isActive = serializers.BooleanField(source="is_active", default=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source="most_recent_active_price",
        read_only=True,
    )
    categoryName = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "price",
            "isActive",
            "updatedAt",
            "createdAt",
            "category",
            "categoryName",
            "prices",
        ]
        read_only_fields = [
            "id",
            "price",
            "prices",
            "updatedAt",
            "createdAt",
            "categoryName",
        ]


class ProductUpdateCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Product` model used for update and create operations.
    """

    isActive = serializers.BooleanField(source="is_active", default=True)
    newPrice = serializers.DecimalField(
        max_digits=10, decimal_places=2, write_only=True, required=False
    )

    class Meta:
        model = Product

        fields = [
            "name",
            "slug",
            "newPrice",
            "category",
            "isActive",
            "newPrice",
        ]

        read_only_fields = [
            "id",
            "updatedAt",
            "createdAt",
        ]

    def create(self, validated_data):
        """
        Create a new product with a new price.
        """
        new_price = validated_data.pop("newPrice", 0)
        product = Product.objects.create(**validated_data)

        # Create a new price
        if new_price is not None:
            Price.objects.create(product=product, amount=new_price)

        return product

    def update(self, instance, validated_data):
        """
        Update an existing product and optionally create new price.
        Perform a partial update, only updating fields that are provided.
        If the new price is the same as the most recent active price, ignore it.
        """
        # Pop the newPrice from the validated data
        new_price = validated_data.pop("newPrice", None)

        # Update product fields that are passed in validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Check if the new price is provided and is different from the most recent price
        if new_price is not None:
            # Fetch the most recent active price for the product
            most_recent_active_price = (
                instance.prices.filter(is_active=True).order_by("-created_at").first()
            )

            # Only create a new price if it's different from the current most recent active price
            if (
                most_recent_active_price is None
                or most_recent_active_price.amount != new_price
            ):
                Price.objects.create(product=instance, amount=new_price)

        return instance

    # def create(self, validated_data):
    #     """
    #     Create a new product and optionally create a new price.
    #     """
    #     new_price = validated_data.pop("newPrice", 0)
    #     product = Product.objects.create(**validated_data)

    #     # Create a new price if provided
    #     if new_price is not None:
    #         print(new_price)
    #         Price.objects.create(product=product, amount=new_price)

    #     return product

    # def update(self, instance, validated_data):
    #     """
    #     Update an existing product and optionally create a new price.
    #     Perform a partial update, only updating fields that are provided.
    #     If the new price is the same as the most recent price, ignore it.
    #     """
    #     # Pop the newPrice from the validated data
    #     new_price = validated_data.pop("newPrice", None)

    #     # Update product fields that are passed in validated_data
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()

    #     # Check if the new price is provided and is different from the most recent price
    #     if new_price is not None:
    #         # Fetch the most recent price for the product
    #         most_recent_price = instance.prices.order_by("-created_at").first()

    #         # Only create a new price if it's different from the current most recent price
    #         if most_recent_price is None or most_recent_price.amount != new_price:
    #             Price.objects.create(product=instance, amount=new_price)

    #     return instance
