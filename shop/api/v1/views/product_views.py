from shop.models import Product
from shop.serializers import ProductSerializer, ProductDetailSerializer

from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ProductListView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    lookup_field = "slug"
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
