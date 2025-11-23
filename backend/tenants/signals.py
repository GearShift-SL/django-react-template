from django.db.models.signals import post_delete
from django.dispatch import receiver
from tenants.models import TenantUser


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
