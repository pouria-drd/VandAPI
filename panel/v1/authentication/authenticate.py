from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import exceptions
from rest_framework.authentication import CSRFCheck


def enforce_csrf(request):
    """
    Enforce CSRF validation.
    """
    check = CSRFCheck()
    # populates request.META['CSRF_COOKIE'], which is used in process_view()
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        # CSRF failed, bail with explicit error message
        raise exceptions.PermissionDenied("CSRF Failed: %s" % reason)


class CustomAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Check if the access token is in the cookies
        access_token = request.COOKIES.get("access_token")
        if access_token is None:
            return None

        # Pass the token for validation
        validated_token = self.get_validated_token(access_token)
        return self.get_user(validated_token), validated_token
