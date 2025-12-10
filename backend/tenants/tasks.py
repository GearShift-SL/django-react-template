import logging
from django.conf import settings
from django.utils import timezone
from tenants.models import Invitation
from utils.loops import send_transactional_email_task
from celery import shared_task

log = logging.getLogger(__name__)


@shared_task
def send_invitation_email_task(invitation_pk: int):
    """
    Send an invitation email to a user.
    """

    # Set the template ID
    transactional_id = settings.LOOPS_INVITATION_TRANSACTIONAL_ID

    # Get the email of the invitation
    email = Invitation.objects.get(pk=invitation_pk).email
    if not email:
        log.error(f"Email not found for invitation {invitation_pk}")
        return False

    # Send the invitation email
    success = send_transactional_email_task(
        transactional_id=transactional_id,
        email=email,
    )

    if not success:
        log.error(f"Error sending invitation email to {email}")
        return False

    # Set the invitation as sent
    invitation = Invitation.objects.get(pk=invitation_pk)
    invitation.last_sent_at = timezone.now()
    invitation.save()

    # Return the invitation
    return True
