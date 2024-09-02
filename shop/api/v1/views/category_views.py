from shop.models import Category
from shop.serializers import CategorySerializer, CategoryDetailSerializer

from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class CategoryListView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    lookup_field = "slug"
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
