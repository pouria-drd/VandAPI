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
from panel.models import LoginOtp
from panel.v1.serializers import LoginSerializer, VerifyLoginSerializer
from panel.v1.utils import async_mail_login_otp, async_notify_superusers


logger = getLogger("panel_login_otp")


class LoginView(APIView):
    http_method_names = ["post"]
    permission_classes = [AllowAny]
    # Request rate limit
    throttle_scope = "panel_login"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user: User = serializer.validated_data["user"]
            try:
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
                        f"Info:Panel Login OTP code sent | Detail:user={user.username} | Date:{timezone.now()}"
                    )

                    return Response(
                        data={"detail": "confirm-login-otp", "otpId": otp_instance.id},
                        status=status.HTTP_200_OK,
                    )
            # Handle exceptions
            except Exception as e:
                logger.error(
                    f"Error:Failed Login request | Detail:error={str(e)} | Date:{timezone.now()}"
                )
                return Response(
                    data={"detail": _("خطای ناخواسته‌ای رخ داده است.")},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        # Handle invalid request
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyLoginView(APIView):
    http_method_names = ["post"]
    permission_classes = [AllowAny]
    # request rate limit
    throttle_scope = "panel_verify_login"
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

                    # Generate JWT token and update last login
                    jwt_token = otp_user.generate_jwt_token()
                    update_last_login(None, otp_user)
                    # Send an alert email to all active superusers asynchronously
                    async_notify_superusers(
                        f"Info:Successful panel login | Detail:user={otp_user.username} | Date:{timezone.now()}"
                    )

                    return Response(
                        data={
                            "refresh": str(jwt_token),
                            "access": str(jwt_token.access_token),
                        },
                        status=status.HTTP_200_OK,
                    )
            # Handle exceptions
            except Exception as e:
                logger.error(
                    f"Error:verifying OTP in panel login failed | Detail:error={str(e)} | Date:{timezone.now()}"
                )
                return Response(
                    {"detail": _("خطای داخلی سرور رخ داده است.")},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        # Handle invalid request
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
