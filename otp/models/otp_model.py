import os
import uuid
import hashlib
from random import choices
from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

OTP_CODE_EXPIRE_TIME = int(os.environ.get("OTP_CODE_EXPIRE_TIME", 5))


def get_default_expires_at():
    return timezone.now() + timedelta(minutes=OTP_CODE_EXPIRE_TIME)


class OTP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Store hashed OTP
    code = models.CharField(_("code"), max_length=256)
    # Number of verification attempts
    attempts = models.IntegerField(_("attempts"), default=0)
    # Max allowed attempts
    max_attempts = models.IntegerField(_("max attempts"), default=3)

    is_active = models.BooleanField(_("is active"), default=True, db_index=True)
    is_verified = models.BooleanField(_("is verified"), default=False)

    expires_at = models.DateTimeField(_("expires at"), default=get_default_expires_at)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    last_attempted = models.DateTimeField(_("last attempted"), auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
        verbose_name = _("OTP code")
        verbose_name_plural = _("OTP codes")

    def is_expired(self) -> bool:
        """Check if the OTP has expired."""
        result: bool = timezone.now() > self.expires_at
        return result

    def has_attempts_left(self) -> bool:
        """Check if the OTP has attempts left."""
        result: bool = self.attempts < self.max_attempts
        return result

    @staticmethod
    def generate_otp_code(length=6) -> str:
        """Generate a random 6-digit OTP code."""
        code: str = "".join(choices("0123456789", k=length))
        return code

    @staticmethod
    def hash_otp(otp: str) -> str:
        """Hash the OTP code using SHA-256."""
        hashed_otp: str = hashlib.sha256(otp.encode()).hexdigest()
        return hashed_otp

    def check_otp(self, otp_code) -> bool:
        """Compare the OTP code with the stored OTP code."""
        result: bool = self.hash_otp(otp_code) == self.code
        return result

    def save(self, *args, **kwargs):
        if not self.code:
            raise ValueError(
                "OTP code cannot be empty"
            )  # If OTP code is not already hashed
        super().save(*args, **kwargs)
