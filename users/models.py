import uuid
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Validator to ensure the username contains only lowercase letters, numbers, and underscores,
# and is no longer than 25 characters.
username_validator = RegexValidator(
    regex=r"^[a-z0-9_]{1,25}$",
    message=_(
        "Username can only contain lowercase letters, numbers, and underscores and must be at most 25 characters long."
    ),
    code="invalid_username",
)


class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    This model uses a UUID as the primary key, requires a username, and makes the
    first name, last name  and email optional.
    """

    # UUID field used as the primary key, automatically generated and not editable by users.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Username field with a custom validator and a maximum length of 25 characters.
    username = models.CharField(
        _("username"),
        unique=True,  # Ensures that each username is unique.
        max_length=25,
        validators=[
            username_validator
        ],  # Applies the custom validator to the username.
        help_text=_("Required. 25 characters or fewer. Letters, digits and _ only."),
    )

    # Optional last name field, can be left blank or set to null.
    last_name = models.CharField(max_length=30, blank=True, null=True)

    # Optional first name field, can be left blank or set to null.
    first_name = models.CharField(max_length=30, blank=True, null=True)

    # Optional email field, can be left blank or set to null.
    email = models.EmailField(_("email address"), blank=True, null=True)

    def __str__(self):
        """
        String representation of the User model.
        Returns the username of the user.
        """
        return self.username
