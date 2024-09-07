from panel.models import Category
from panel.serializers import CategorySerializer

from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


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
    queryset = Category.objects.all()


class CategoryDetailUpdateView(RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, deleting and updating a single `Category` instance.

    This view supports GET requests to retrieve a category and PATCH requests
    to update an existing category and DELETE requests to delete a category.

    HTTP Methods:
    - GET: Retrieve details of a specific category.
    - PATCH: Update an existing category.
    - DELETE: Delete a category.
    """

    lookup_field = "slug"
    http_method_names = ["get", "patch", "delete"]
    serializer_class = CategorySerializer
    # Fetch products and their prices for efficient querying
    queryset = Category.objects.prefetch_related("products__prices")


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
