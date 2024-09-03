from shop.models import Category
from shop.serializers import CategorySerializer, CategoryUpdateSerializer

from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView


class CategoryListCreateView(ListCreateAPIView):
    http_method_names = ["get", "post"]
    serializer_class = CategorySerializer
    # Fetch products and their prices
    queryset = Category.objects.prefetch_related("products__prices")


class CategoryDetailUpdateView(RetrieveUpdateAPIView):
    lookup_field = "slug"
    http_method_names = ["get", "patch"]
    # Fetch products and their prices
    queryset = Category.objects.prefetch_related("products__prices")

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return CategoryUpdateSerializer
        return CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
