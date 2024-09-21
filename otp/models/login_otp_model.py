from otp.models import OTP
from users.models import User

from django.db import models
from django.utils.translation import gettext_lazy as _


class LoginOtp(OTP):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="login_otp_codes", db_index=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("login OTP code")
        verbose_name_plural = _("login OTP codes")

    def __str__(self) -> str:
        return f"Login OTP for {self.user.username}"
