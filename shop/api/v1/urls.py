from django.urls import path
from shop.api.v1.views import ProductListView, ProductDetailView
from shop.api.v1.views import CategoryListView, CategoryDetailView

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path(
        "categories/<slug:slug>/", CategoryDetailView.as_view(), name="category-detail"
    ),
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
]
