import logging


from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from tenants.models import Tenant, TenantUser, Invitation, TenantUserRole
from tenants.tasks import send_invitation_email_task
from allauth.account.signals import user_signed_up
from django.utils import timezone

log = logging.getLogger(__name__)


@receiver(post_delete, sender=TenantUser)
def on_tenant_user_deleted(sender, instance, **kwargs):
    """
    When a TenantUser is deleted, check if the tenant has any remaining users.
    If not, delete the tenant as well.
    """
    tenant = instance.tenant
    if not tenant:
        return

    # If there are no remaining users for this tenant, remove the tenant.
    # Using post_delete ensures the current TenantUser is already gone.
    if not tenant.tenant_users.exists():
        tenant.delete()


# Function to send an invitation email to a user
@receiver(post_save, sender=Invitation)
def on_invitation_saved(sender, instance, created, **kwargs):
    """
    When an Invitation is saved, send an invitation email to the user.
    """
    if not created:
        return

    send_invitation_email_task.delay(instance.pk)


@receiver(user_signed_up)
def on_user_signed_up(sender, request, user, **kwargs):
    """
    Handle tenant creation and user invitation acceptance:
        1. If there's an existing invitation, create a tenant user for that tenant
        2. Otherwise, create a new tenant and tenant user for the current user
    """

    # Check if there's an existing invitation for this user's email
    try:
        invitation = Invitation.objects.get(email=user.email, accepted_at__isnull=True)

        # Create a tenant user for the invited tenant
        TenantUser.objects.create(
            user=user, tenant=invitation.tenant, role=TenantUserRole.USER
        )

        # Mark the invitation as accepted
        invitation.accepted_at = timezone.now()
        invitation.save()

        log.info(
            f"User {user.email} signed up via invitation to tenant {invitation.tenant.name}"
        )
    except Invitation.DoesNotExist:
        # No invitation found, create a new tenant for the user
        # Use first name if available, otherwise fall back to email
        if user.first_name:
            tenant_name = f"{user.first_name}'s team"
        else:
            tenant_name = f"{user.email.split('@')[0]}'s team"

        tenant = Tenant.objects.create(name=tenant_name)
        TenantUser.objects.create(user=user, tenant=tenant, role=TenantUserRole.OWNER)

        log.info(f"User {user.email} signed up and created new tenant {tenant.name}")
