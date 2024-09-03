from django.urls import path

from panel.api.v1.views import PriceListView, PriceDetailView
from panel.api.v1.views import ProductListView, ProductDetailView
from panel.api.v1.views import CategoryListCreateView, CategoryDetailUpdateView

urlpatterns = [
    # prices urls
    path("prices/", PriceListView.as_view(), name="price-list"),
    path("prices/<uuid:pk>/", PriceDetailView.as_view(), name="price-detail"),
    # products urls
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
    # categories urls
    path("categories/", CategoryListCreateView.as_view(), name="category-list"),
    path(
        "categories/<slug:slug>/",
        CategoryDetailUpdateView.as_view(),
        name="category-detail",
    ),
]
