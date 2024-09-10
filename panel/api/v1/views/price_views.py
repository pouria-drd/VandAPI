from panel.models import Price
from panel.api.v1.serializers import PriceSerializer

from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class PriceListView(ListCreateAPIView):
    """
    View for listing and creating `Price` instances.

    This view supports GET requests to list all price entries and POST requests
    to create a new price entry.

    HTTP Methods:
    - GET: List all prices.
    - POST: Create a new price.
    """

    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    http_method_names = ["get", "post"]


class PriceDetailView(RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a single `Price` instance.

    This view supports GET requests to retrieve a price entry, PUT/PATCH requests
    to update an existing price entry, and DELETE requests to remove a price entry.

    HTTP Methods:
    - GET: Retrieve details of a specific price.
    - PUT/PATCH: Update an existing price.
    - DELETE: Delete a price entry.
    """

    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    http_method_names = ["get", "delete"]


class PriceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing `Price` instances.

    This viewset provides CRUD operations for price entries using the standard
    HTTP methods. It supports listing, retrieving, creating, updating, and
    deleting price entries.

    HTTP Methods:
    - GET: List all prices or retrieve a specific price.
    - POST: Create a new price entry.
    - PUT/PATCH: Update an existing price entry.
    - DELETE: Delete a price entry.
    """

    queryset = Price.objects.all()
    serializer_class = PriceSerializer
