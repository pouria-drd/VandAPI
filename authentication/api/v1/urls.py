from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from authentication.api.v1.views import LoginView, VerifyLoginView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login-v1"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("verify-login/", VerifyLoginView.as_view(), name="verify-login-v1"),
]
