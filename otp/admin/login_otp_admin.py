from otp.models import LoginOtp
from django.contrib import admin


@admin.register(LoginOtp)
class LoginOtpAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        # bools
        "is_verified",
        "is_active",
        "is_expired",
        # ints
        "attempts",
        "max_attempts",
        # datetimes
        "last_attempted",
        "created_at",
        "expires_at",
    )
    readonly_fields = (
        "code",
        # bools
        "is_verified",
        "is_active",
        "is_expired",
        # ints
        "attempts",
        "max_attempts",
        # datetimes
        "last_attempted",
        "created_at",
        "expires_at",
    )
    search_fields = ("user__username",)
    list_filter = ("user", "is_active", "created_at", "expires_at")

    def is_expired(self, obj):
        """Display whether the OTP is expired."""
        return obj.is_expired()

    is_expired.boolean = True
    is_expired.short_description = "Expired"

    def has_change_permission(self, request, obj=None):
        """Restrict edit permissions for the OTP code."""
        if obj:
            return False  # Prevent editing of OTP codes
        return super().has_change_permission(request, obj)
