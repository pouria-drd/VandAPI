from django.urls import path
from menu.api.v1.views import (
    MenuListView,
    MenuDetailView,
)

urlpatterns = [
    path("", MenuListView.as_view(), name="menu-list"),
    path(
        "<slug:slug>/",
        MenuDetailView.as_view(),
        name="menu-detail",
    ),
]
