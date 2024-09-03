from shop.models import Price
from rest_framework import serializers


class PriceSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Price` model used for read and write operations.

    This serializer includes fields for price details such as amount, product,
    and active status. It also includes read-only fields for timestamps.
    """

    isActive = serializers.BooleanField(source="is_active", default=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Price
        fields = [
            "id",
            "amount",
            "product",
            "isActive",
            "updatedAt",
            "createdAt",
        ]
        read_only_fields = ["id", "createdAt", "updatedAt"]
