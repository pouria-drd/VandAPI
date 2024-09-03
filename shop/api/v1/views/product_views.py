from shop.models import Product, Price
from shop.serializers import ProductSerializer, ProductUpdateSerializer

from rest_framework import viewsets
from django.db.models import OuterRef, Subquery
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ProductListView(ListCreateAPIView):
    queryset = Product.objects.annotate(
        most_recent_price=Subquery(
            Price.objects.filter(product=OuterRef("pk"))
            .order_by("-created_at")
            .values("amount")[:1]
        )
    ).prefetch_related("prices")
    serializer_class = ProductSerializer
    http_method_names = ["get", "post"]


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    lookup_field = "slug"
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ["get", "patch", "delete"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductSerializer
        return ProductUpdateSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
