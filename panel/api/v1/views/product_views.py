from panel.models import Product, Price
from panel.api.v1.serializers import (
    ProductSerializer,
    ProductDetailSerializer,
    ProductUpdateCreateSerializer,
)

from rest_framework import viewsets
from django.db.models import OuterRef, Subquery
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ProductListView(ListCreateAPIView):
    """
    View for listing and creating `Product` instances.

    HTTP Methods:
    - GET: List all products with their most recent active price.
    - POST: Create a new product.
    """

    serializer_class = ProductSerializer
    http_method_names = ["get", "post"]

    def get_serializer_class(self):
        """
        Determine the serializer class based on the request method.
        Returns:
            ProductUpdateCreateSerializer: For POST requests.
            ProductSerializer: For GET requests.
        """
        if self.request.method == "POST":
            return ProductUpdateCreateSerializer
        return ProductSerializer

    def get_queryset(self):
        """
        Annotate each Product with the most recent active price and include the category data
        """
        return (
            Product.objects.annotate(
                most_recent_active_price=Subquery(
                    Price.objects.filter(
                        product=OuterRef("pk"), is_active=True
                    )  # Filter active prices for each product
                    .order_by(
                        "-created_at"
                    )  # Order by creation date to get the latest price
                    .values("amount")[:1]
                )
            )
            .select_related("category")  # Include the related category in the query
            .prefetch_related("prices")
        )  # Prefetch related prices to optimize queries


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a single `Product` instance.

    HTTP Methods:
    - GET: Retrieve details of a specific product.
    - PATCH: Update an existing product.
    - DELETE: Delete a product.
    """

    lookup_field = "slug"  # Use slug to identify the product
    http_method_names = ["get", "patch", "delete"]

    def get_serializer_class(self):
        """
        Determine the serializer class based on the request method.
        Returns:
            ProductSerializer: For GET requests.
            ProductUpdateCreateSerializer: For PATCH requests.
        """
        if self.request.method == "PATCH":
            return ProductUpdateCreateSerializer
        return ProductDetailSerializer

    def get_queryset(self):
        """
        Annotate each Product with the most recent active price using a Subquery
        """
        return Product.objects.annotate(
            most_recent_active_price=Subquery(
                Price.objects.filter(
                    product=OuterRef("pk"), is_active=True
                )  # Filter active prices for each product
                .order_by(
                    "-created_at"
                )  # Order by creation date to get the latest price
                .values("amount")[:1]  # Select the amount of the most recent price
            )
        ).prefetch_related(
            "prices"
        )  # Prefetch related prices to optimize queries


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing `Product` instances.
    """

    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
