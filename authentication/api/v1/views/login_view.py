from logging import getLogger
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle

from django.utils import timezone
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import update_last_login

from users.models import User
from otp.models import LoginOtp
from authentication.api.v1.serializers import LoginSerializer, VerifyLoginSerializer
from mail.utils import (
    async_mail_login_otp,
    async_notify_superusers,
    async_notify_user,
)


logger = getLogger("login_v1")


class LoginView(APIView):
    http_method_names = ["post"]
    permission_classes = [AllowAny]
    # Request rate limit
    throttle_scope = "login_v1"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user: User = serializer.validated_data["user"]
            try:
                # If not an admin user
                if not user.is_staff:
                    # Generate token
                    token = user.generate_jwt_token()
                    refresh_token = str(token)
                    access_token = str(token.access_token)
                    # update last login and send a security alert to user
                    update_last_login(None, user)
                    async_notify_user(
                        user,
                        f"Dear {user.username}, you have been logged in to the Cafe Vand website. If this action was not initiated by you, please contact the website administrator immediately.",
                    )
                    logger.info(
                        f"Info:Login successful | Detail:user={user.username} | Date:{timezone.now()}"
                    )
                    return Response(
                        data={
                            "access": access_token,
                            "refresh": refresh_token,
                        },
                        status=status.HTTP_200_OK,
                    )
                # If an admin user
                with transaction.atomic():
                    # Create an OTP and send it to the user’s email
                    otp_code = LoginOtp.generate_otp_code()
                    hashed_otp_code = LoginOtp.hash_otp(otp_code)
                    otp_instance = LoginOtp.objects.create(
                        user=user, code=hashed_otp_code
                    )
                    # Send OTP to the user’s email asynchronously
                    async_mail_login_otp(otp_instance.user, otp_code)
                    # Send an alert email to all active superusers asynchronously
                    async_notify_superusers(
                        f"Info:Login OTP sent | Detail:user={user.username} | Date:{timezone.now()}"
                    )
                    logger.info(
                        f"Info:Login OTP sent | Detail:user={user.username} | Date:{timezone.now()}"
                    )
                    return Response(
                        data={
                            "otpId": otp_instance.id,
                            "detail": "confirm-login-otp",
                        },
                        status=status.HTTP_200_OK,
                    )
            # Handle exceptions
            except Exception as e:
                logger.error(
                    f"Error:Login request failed | Detail:error={str(e)} | Date:{timezone.now()}"
                )
                return Response(
                    data={"detail": _("Internal server error occurred.")},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        # Handle invalid request
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyLoginView(APIView):
    http_method_names = ["post"]
    permission_classes = [AllowAny]
    # request rate limit
    throttle_scope = "verify_login_v1"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request):
        serializer = VerifyLoginSerializer(data=request.data)
        if serializer.is_valid():
            otp_user: User = serializer.validated_data["otp_user"]
            otp_instance: LoginOtp = serializer.validated_data["otp_instance"]
            try:
                with transaction.atomic():
                    # OTP is verified, mark OTP as verified and save
                    otp_instance.is_active = False
                    otp_instance.is_verified = True
                    otp_instance.save()

                    # Generate JWT tokens
                    token = otp_user.generate_jwt_token()
                    refresh_token = str(token)
                    access_token = str(token.access_token)
                    # update last login and send security alerts
                    update_last_login(None, otp_user)
                    async_notify_user(
                        otp_user,
                        f"Dear {otp_user.username}, you have been logged in to the Cafe Vand website. If this action was not initiated by you, please contact the website administrator immediately.",
                    )
                    # Send an alert email to all active superusers asynchronously
                    async_notify_superusers(
                        f"Info:Successful verify login | Detail:user={otp_user.username} | Date:{timezone.now()}"
                    )
                    logger.error(
                        f"Info:Successful verify login | Detail:user={otp_user.username} | Date:{timezone.now()}"
                    )
                    return Response(
                        data={
                            "access": access_token,
                            "refresh": refresh_token,
                        },
                        status=status.HTTP_200_OK,
                    )
            # Handle exceptions
            except Exception as e:
                print(str(e))
                logger.error(
                    f"Error:verifying login OTP failed | Detail:error={str(e)} | Date:{timezone.now()}"
                )
                return Response(
                    {"detail": _("Internal server error occurred.")},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        # Handle invalid request
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
