import threading
from logging import getLogger
from users.models import User

from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail


logger = getLogger("panel_login_otp")


class EmailThread(threading.Thread):
    """Thread for sending emails asynchronously."""

    def __init__(
        self,
        subject: str,
        message: str,
        from_email: str,
        recipient_list: list,
        fail_silently=False,
        is_admin_alert=False,
    ):
        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.recipient_list = recipient_list
        self.fail_silently = fail_silently
        self.is_admin_alert = is_admin_alert
        threading.Thread.__init__(self)

    def run(self):
        try:
            send_mail(
                subject=self.subject,
                message=self.message,
                from_email=self.from_email,
                recipient_list=self.recipient_list,
                fail_silently=self.fail_silently,
            )
            if self.is_admin_alert:
                logger.info(
                    f"Info:Async email sent | Detail:subject={self.subject} | Date:{timezone.now()}"
                )
            else:
                logger.info(
                    f"Info:Async email sent | Detail:subject={self.subject}, emails={self.recipient_list} | Date:{timezone.now()}"
                )

        except Exception as e:
            logger.error(
                f"Error:Failed to send async email | Detail:subject={self.subject}, error={str(e)} | Date:{timezone.now()}"
            )


def async_mail_login_otp(user: User, otp_code: str):
    """Send an OTP to the user’s email asynchronously."""
    user_email = user.email
    username = user.username
    subject = "Cafe Vand Login Code"
    message = f"Welcome {username}! Your login code is: {otp_code}"

    # Send OTP asynchronously
    EmailThread(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        is_admin_alert=False,
    ).start()


def async_notify_superusers(message: str):
    """Send an alert email to all active superusers asynchronously."""
    subject = "Cafe Vand Admins Alert!"

    superusers_emails = User.objects.filter(
        is_superuser=True, is_active=True
    ).values_list("email", flat=True)

    if superusers_emails:
        # Send OTP asynchronously
        EmailThread(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=superusers_emails,
            is_admin_alert=True,
        ).start()


def mail_login_otp(user: User, otp_code: str):
    """Send an OTP to the user’s email."""

    user_email = user.email
    username = user.username
    subject = "Cafe Vand Login Code"
    message = f"Welcome {username}! Your login code is: {otp_code}"

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
        )
        logger.info(
            f"Info:Login OTP sent | Detail:user={username}, emails={user_email} | Date:{timezone.now()}"
        )

    except Exception as e:
        logger.error(
            f"Error:Failed to send login otp | Detail:user={username}, emails={user_email}, error={str(e)} | Date:{timezone.now()}"
        )
        raise e


def notify_superusers(message: str):
    """Send an alert email to all active superusers."""
    subject = "Cafe Vand Admin Alert!"

    try:
        superusers_emails = User.objects.filter(
            is_superuser=True, is_active=True
        ).values_list("email", flat=True)

        if superusers_emails:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=superusers_emails,
            )
            logger.info(f"Info:Admin alert sent | Date:{timezone.now()}")

    except Exception as e:
        logger.error(
            f"Error:Failed to send alert to superusers | Detail:error={str(e)} | Date:{timezone.now()}"
        )
        raise e
