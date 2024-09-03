from shop.models import Category
from menu.serializers import MenuCategorySerializer, MenuCategoryDetailSerializer

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet


class MenuListView(ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = MenuCategorySerializer
    http_method_names = ["get"]


class MenuDetailView(RetrieveAPIView):
    lookup_field = "slug"
    queryset = Category.objects.filter(is_active=True)
    serializer_class = MenuCategoryDetailSerializer
    http_method_names = ["get"]


class MenuViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = MenuCategorySerializer
    http_method_names = ["get"]
