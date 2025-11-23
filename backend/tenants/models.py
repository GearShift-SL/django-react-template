import random
import string
from django.conf import settings
from django.db import models
from django.forms import ValidationError
from django.utils.text import slugify


class Tenant(models.Model):
    name = models.CharField(max_length=100, unique=False)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    # Contact fields
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Code to create the unique slug for the tenant upon save
        if not self.pk:
            self.slug = slugify(self.name)
            while Tenant.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.name)}-{random.randint(0, 1000)}"
        super().save(*args, **kwargs)


class TenantLogo(models.Model):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name="logo")
    image = models.ImageField(upload_to="tenants/logos/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tenant.name} logo"


class TenantModel(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def clean(self):
        if not self.tenant:
            raise ValidationError("A tenant is required")


class TenantUser(models.Model):
    """
    Model to store the relationship between a user and a tenant
    with the role of the user in the tenant.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tenant_user"
    )
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="tenant_users"
    )
    ROLE_OPTIONS = [
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("user", "User"),
    ]
    role = models.CharField(max_length=30, choices=ROLE_OPTIONS, default="user")

    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.email = self.user.email
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.tenant.name} - {self.role}"


# Invitations model to store the invitations sent to users by owners or admins
class Invitation(models.Model):
    # The email of the user to be invited
    email = models.EmailField(unique=True)

    # The user who sent the invitation
    invited_by = models.ForeignKey(
        TenantUser, on_delete=models.CASCADE, related_name="invitations_sent"
    )

    # A random generated code
    code = models.CharField(max_length=32, blank=True, null=True)

    # If the invitation is accepted/disabled
    is_accepted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    # Create a random code and save it in the database
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super().save(*args, **kwargs)

    def generate_code(self):
        return "".join(random.choices(string.ascii_letters + string.digits, k=32))

    def clean(self):
        # Check if the email is already in use
        if TenantUser.objects.filter(user__email=self.email).exists():
            raise ValidationError("The email is already in use")
