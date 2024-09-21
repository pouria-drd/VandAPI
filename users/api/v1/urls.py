from django.urls import path
from users.api.v1.views import MeView


urlpatterns = [
    path("me/", MeView.as_view(), name="me-v1"),
]
