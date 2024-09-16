from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from panel.v1.views import (
    # login views
    LoginView,
    VerifyLoginView,
    # prices views
    PriceListView,
    PriceDetailView,
    # products views
    ProductListView,
    ProductDetailView,
    # categories views
    CategoryListCreateView,
    CategoryDetailUpdateView,
)


urlpatterns = [
    # login urls
    path("login/", LoginView.as_view(), name="panel-login"),
    path("verify-login/", VerifyLoginView.as_view(), name="panel-verify-login"),
    path("refresh/", TokenRefreshView.as_view(), name="panel-refresh"),
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
