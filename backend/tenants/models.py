import random
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


class TenantUserRole(models.TextChoices):
    OWNER = "owner", "Owner"
    ADMIN = "admin", "Admin"
    USER = "user", "User"


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
    role = models.CharField(
        max_length=30, choices=TenantUserRole.choices, default=TenantUserRole.USER
    )

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
class Invitation(TenantModel):
    # The email of the user to be invited
    email = models.EmailField(unique=True)

    # The user who sent the invitation
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="invitations_sent",
    )

    # Last sent at date and time
    last_sent_at = models.DateTimeField(blank=True, null=True)

    # If the invitation is accepted, the date and time of the acceptance
    accepted_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    def clean(self):
        # Check if the email is already in use
        if TenantUser.objects.filter(user__email=self.email).exists():
            raise ValidationError("The email is already in use")
