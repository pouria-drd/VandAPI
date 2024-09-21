from django.urls import path
from menu.api.v1.views import (
    MenuListView,
    MenuDetailView,
    PriceListView,
    PriceDetailView,
    ProductListCreateView,
    ProductDetailUpdateView,
    CategoryListCreateView,
    CategoryDetailUpdateView,
)

urlpatterns = [
    # menu urls
    path("", MenuListView.as_view(), name="menu-list-v1"),
    path(
        "<slug:slug>/",
        MenuDetailView.as_view(),
        name="menu-detail",
    ),
    # prices urls
    path("prices/", PriceListView.as_view(), name="price-list-v1"),
    path("prices/<uuid:pk>/", PriceDetailView.as_view(), name="price-detail-v1"),
    # products urls
    path("products/", ProductListCreateView.as_view(), name="product-list-v1"),
    path(
        "products/<slug:slug>/",
        ProductDetailUpdateView.as_view(),
        name="product-detail",
    ),
    # categories urls
    path("categories/", CategoryListCreateView.as_view(), name="category-list-v1"),
    path(
        "categories/<slug:slug>/",
        CategoryDetailUpdateView.as_view(),
        name="category-detail",
    ),
]
