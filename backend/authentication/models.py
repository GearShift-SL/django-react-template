# django
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

# Local App
from .managers import EmailUsernameUserManager
from .utils import avatar_upload_path

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

    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        # Process avatar image if it's being uploaded or changed
        if self.avatar:
            # Check if this is a new upload or changed avatar
            # We need to process it if: 1) it's a new instance, or 2) the avatar field has changed
            try:
                old_instance = UserProfile.objects.get(pk=self.pk)
                avatar_changed = old_instance.avatar != self.avatar
            except UserProfile.DoesNotExist:
                # New instance, avatar needs processing
                avatar_changed = True

            if avatar_changed:
                from .utils import process_avatar_image

                processed_image = process_avatar_image(self.avatar, self.user.pk)
                if processed_image:
                    self.avatar = processed_image

        super().save(*args, **kwargs)
