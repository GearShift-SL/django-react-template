"""
singnals.py

This file contains the signals for the authentication app.
"""

from django.dispatch import receiver
from allauth.account.signals import user_signed_up, email_confirmed
from django.db.models.signals import pre_save, post_save
from django.contrib.auth import get_user_model
from django.db import transaction
from tenants.models import Tenant, TenantUser
from utils.loops import create_contact_task, update_or_create_contact_task
from .models import UserProfile


import logging

log = logging.getLogger(__name__)


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a UserProfile when a new User is created.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(user_signed_up)
def on_user_signed_up(sender, request, user, **kwargs):
    """
    Trigger stuff when a user signs up:
        1. Create a tenant and tenant user for the current user
    """
    log.debug(f"Request: {request}")

    # Create a tenant and tenant user for the current user
    # Use first name if available, otherwise fall back to email
    if user.first_name:
        tenant_name = f"{user.first_name}'s team"
    else:
        tenant_name = f"{user.email.split('@')[0]}'s team"

    tenant = Tenant.objects.create(name=tenant_name)
    TenantUser.objects.create(user=user, tenant=tenant, role="owner")


@receiver(email_confirmed)
def on_email_confirmed(sender, request, email_address, **kwargs):
    """
    Trigger stuff when a user verifies their email:
        1. Create an audience member in Loops
    """
    log.debug(f"Request: {request}")

    update_or_create_contact_task.delay(
        email=email_address.email,
        firstName=email_address.user.first_name,
        lastName=email_address.user.last_name,
        source="app",
        subscribed=True,
        userGroup="app",
        userId=email_address.user.id,
    )


@receiver(pre_save, sender=get_user_model())
def on_user_name_updated(sender, instance, **kwargs):
    """
    When a user updates their first and/or last name, sync the Loops contact.
    Uses pre_save to detect changes and enqueues the task on transaction commit.
    """
    # New instance, nothing to compare
    if not instance.pk:
        return

    try:
        previous = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    first_name_changed = previous.first_name != instance.first_name
    last_name_changed = previous.last_name != instance.last_name

    if not (first_name_changed or last_name_changed):
        return

    def enqueue_update():
        update_or_create_contact_task.delay(
            email=instance.email,
            firstName=instance.first_name,
            lastName=instance.last_name,
            source="app",
            subscribed=True,
            userGroup="app",
            userId=instance.id,
        )

    # Send the task to update the Loops contact info after the transaction commits
    # This ensures the user's updated name is saved before syncing to Loops
    transaction.on_commit(enqueue_update)
