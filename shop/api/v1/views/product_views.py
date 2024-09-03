from shop.models import Product, Price
from shop.serializers import ProductSerializer, ProductUpdateSerializer

from rest_framework import viewsets
from django.db.models import OuterRef, Subquery
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ProductListView(ListCreateAPIView):
    """
    View for listing and creating `Product` instances.

    This view supports GET requests to list all products and POST requests
    to create a new product. Products are annotated with the most recent
    price using a subquery for efficient retrieval.

    HTTP Methods:
    - GET: List all products with their most recent price.
    - POST: Create a new product.
    """

    # Annotate each Product with the most recent price using a Subquery
    queryset = Product.objects.annotate(
        most_recent_price=Subquery(
            Price.objects.filter(
                product=OuterRef("pk")
            )  # Filter prices for each product
            .order_by("-created_at")  # Order by creation date to get the latest price
            .values("amount")[:1]  # Select the amount of the most recent price
        )
    ).prefetch_related(
        "prices"
    )  # Prefetch related prices to optimize queries
    serializer_class = ProductSerializer
    http_method_names = ["get", "post"]


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a single `Product` instance.

    This view supports GET requests to retrieve a product, PATCH requests
    to update an existing product, and DELETE requests to remove a product.

    HTTP Methods:
    - GET: Retrieve details of a specific product.
    - PATCH: Update an existing product.
    - DELETE: Delete a product.
    """

    lookup_field = "slug"  # Use slug to identify the product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ["get", "patch", "delete"]

    def get_serializer_class(self):
        """
        Determine the serializer class based on the request method.

        Returns:
            ProductSerializer: For GET requests.
            ProductUpdateSerializer: For PATCH requests.
        """
        if self.request.method == "PATCH":
            return ProductUpdateSerializer
        return ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing `Product` instances.

    This viewset provides CRUD operations for products using the standard
    HTTP methods. It supports listing, retrieving, creating, updating, and
    deleting products.

    HTTP Methods:
    - GET: List all products or retrieve a specific product.
    - POST: Create a new product.
    - PUT/PATCH: Update an existing product.
    - DELETE: Delete a product.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
