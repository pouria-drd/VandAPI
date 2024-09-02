from shop.models import Price
from shop.serializers import PriceSerializer

from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class PriceListView(ListCreateAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer


class PriceDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    http_method_names = ["get", "patch", "delete"]


class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
