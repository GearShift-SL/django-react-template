from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from tenants.models import TenantUser, Invitation
from tenants.tasks import send_invitation_email_task


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
