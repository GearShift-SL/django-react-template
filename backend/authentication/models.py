# django
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

# Local App
from .managers import EmailUsernameUserManager

# User model in case we want to add more fields in the future
# class User(AbstractUser):
#     pass


# User model with email as the unique identifier
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = EmailUsernameUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name:
            return self.first_name
        else:
            return ""


# User Profile class to store additional user information if needed
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return self.user.email
