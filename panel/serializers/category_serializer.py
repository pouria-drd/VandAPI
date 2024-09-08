import os
import base64
from dotenv import load_dotenv

from rest_framework import serializers
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _

from panel.models import Category
from panel.serializers.product_serializer import ProductSerializer
from panel.panel_settings import Category_ICON_MAX_SIZE as size_limit

load_dotenv()  # Loads the variables from the .env file into the environment

# Load allowed extensions from environment variable
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS", "png,jpg,jpeg").split(",")


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model, used for creating and reading category instances.
    """

    icon = serializers.CharField(required=False, allow_null=True)
    isActive = serializers.BooleanField(source="is_active", default=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        """
        Meta class to configure the serializer's model and fields.
        """

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
            "updatedAt",
            "createdAt",
            "products",
        ]  # Read-only fields

    def validate_icon(self, value):
        """
        Validate the icon field to ensure it meets the size and extension requirements.

        Args:
            value (str): Base64 encoded image string.

        Returns:
            ContentFile: Validated image file if valid.

        Raises:
            serializers.ValidationError: If the image file is too large or has an invalid extension.
        """
        if value:
            # Decode base64 string
            format, imgstr = value.split(";base64,")
            ext = format.split("/")[-1]  # Extract file extension
            print(ALLOWED_EXTENSIONS)

            # Validate file extension
            if ext not in ALLOWED_EXTENSIONS:
                raise serializers.ValidationError(
                    _(f"Supported formats are: {', '.join(ALLOWED_EXTENSIONS)}.")
                )

            data = base64.b64decode(imgstr)  # Decode the image data
            file = ContentFile(data, name=f"image.{ext}")  # Create a ContentFile object

            # Validate the size
            if file.size > size_limit:
                raise serializers.ValidationError(
                    _(
                        f"Image file is too large (more than {size_limit / 1024 / 1024} MB) !"
                    )
                )

            return file
        return value


class CategoryDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model, used for creating and reading category instances.
    """

    icon = serializers.ImageField()
    isActive = serializers.BooleanField(source="is_active", default=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class to configure the serializer's model and fields.
        """

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
            "updatedAt",
            "createdAt",
            "products",
        ]  # Read-only fields
