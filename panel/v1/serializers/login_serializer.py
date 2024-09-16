from logging import getLogger
from rest_framework import serializers

from django.utils import timezone
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from users.models import User
from panel.models import LoginOtp
from panel.v1.utils import async_notify_superusers


logger = getLogger("panel_login_otp")


class LoginSerializer(serializers.Serializer):
    """
    Serializer for authenticating a user.
    """

    username = serializers.CharField(
        required=True,
        min_length=3,
        max_length=30,
        error_messages={
            "required": _("نام کاربری الزامی است."),
            "blank": _("نام کاربری نمی‌تواند خالی باشد."),
            "min_length": _("نام کاربری باید حداقل 3 کاراکتر باشد."),
            "max_length": _("نام کاربری باید حداکثر 30 کاراکتر باشد."),
        },
    )
    password = serializers.CharField(
        required=True,
        min_length=8,
        write_only=True,
        error_messages={
            "required": _("رمز عبور الزامی است."),
            "blank": _("رمز عبور نمی‌تواند خالی باشد."),
            "min_length": _("رمز عبور باید حداقل 8 کاراکتر باشد."),
        },
    )

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is None or not user.is_active or not user.is_staff:
            raise serializers.ValidationError(
                {"detail": _("نام کاربری یا رمز عبور اشتباه است.")}
            )
        data["user"] = user
        return data


class VerifyLoginSerializer(serializers.Serializer):
    """Serializer for verifying a user's login otp"""

    otpId = serializers.UUIDField(
        required=True,
        error_messages={
            "required": _("آیدی کد ورود الزامی است."),
            "blank": _("آیدی کد ورود نمی‌تواند خالی باشد."),
            "format": _("آیدی کد ورود معتبر نمی باشد"),
            "invalid": _("آیدی کد ورود معتبر نمی باشد"),
        },
    )
    otpCode = serializers.CharField(
        required=True,
        min_length=6,
        max_length=6,
        error_messages={
            "required": _("کد ورود الزامی است."),
            "blank": _("کد ورود نمی‌تواند خالی باشد."),
            "min_length": _("کد ورود باید حداقل 6 کاراکتر باشد."),
            "max_length": _("کد ورود باید حداکثر 6 کاراکتر باشد."),
        },
    )

    def validate(self, data):
        otp_id = data.get("otpId")
        otp_code = data.get("otpCode")

        # Fetch the OTP record related to the user
        try:
            otp_instance = LoginOtp.objects.get(
                id=otp_id, is_verified=False, is_active=True
            )
            if otp_instance is None:
                raise serializers.ValidationError({"detail": _("کد ورود معتبر نیست.")})
        except LoginOtp.DoesNotExist:
            raise serializers.ValidationError({"detail": _("کد ورود معتبر نیست.")})

        otp_user: User = otp_instance.user

        # Check if all attempts have been used
        if not otp_instance.has_attempts_left():
            # Update the OTP record
            otp_instance.attempts += 1
            otp_instance.is_active = False
            otp_instance.save()
            # Ban the user
            otp_user.is_staff = False
            otp_user.is_active = False
            otp_user.save()
            # Send an alert email to all active superusers and log the event
            message = f"Warning:User has been banned for too many failed login attempts | Detail:user={otp_user.username} | Date:{timezone.now()}"
            logger.warning(message)
            async_notify_superusers(message)

            raise serializers.ValidationError(
                {"detail": _("حساب کاربری شما موقتا مسدود شده است.")},
            )

        # Check if OTP is expired
        if otp_instance.is_expired():
            otp_instance.attempts += 1
            otp_instance.is_active = False
            otp_instance.save()
            raise serializers.ValidationError({"detail": _("کد ورود منقضی شده است.")})

        # Check if the OTP is valid
        if not otp_instance.check_otp(otp_code):
            otp_instance.attempts += 1
            otp_instance.save()
            raise serializers.ValidationError({"detail": _("کد ورود اشتباه است.")})

        data["otp_user"] = otp_user
        data["otp_instance"] = otp_instance
        return data
