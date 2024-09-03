from panel.models import Category
from panel.serializers import CategorySerializer, CategoryUpdateSerializer

from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView


class CategoryListCreateView(ListCreateAPIView):
    """
    View for listing and creating `Category` instances.

    This view supports GET requests to list all categories and POST requests
    to create a new category. It fetches related products and their prices
    to include in the serialized output.

    HTTP Methods:
    - GET: List all categories.
    - POST: Create a new category.
    """

    http_method_names = ["get", "post"]
    serializer_class = CategorySerializer
    # Fetch products and their prices for efficient querying
    queryset = Category.objects.prefetch_related("products__prices")


class CategoryDetailUpdateView(RetrieveUpdateAPIView):
    """
    View for retrieving and updating a single `Category` instance.

    This view supports GET requests to retrieve a category and PATCH requests
    to update an existing category. It fetches related products and their prices
    to include in the serialized output. The serializer class is determined based
    on the request method.

    HTTP Methods:
    - GET: Retrieve details of a specific category.
    - PATCH: Update an existing category.
    """

    lookup_field = "slug"
    http_method_names = ["get", "patch"]
    # Fetch products and their prices for efficient querying
    queryset = Category.objects.prefetch_related("products__prices")

    def get_serializer_class(self):
        """
        Determine the serializer class based on the request method.

        Returns:
            CategorySerializer: For GET requests.
            CategoryUpdateSerializer: For PATCH requests.
        """
        if self.request.method == "PATCH":
            return CategoryUpdateSerializer
        return CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing `Category` instances.

    This viewset provides CRUD operations for categories using the standard
    HTTP methods. It supports listing, retrieving, creating, updating, and
    deleting categories.

    HTTP Methods:
    - GET: List all categories or retrieve a specific category.
    - POST: Create a new category.
    - PUT/PATCH: Update an existing category.
    - DELETE: Delete a category.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
