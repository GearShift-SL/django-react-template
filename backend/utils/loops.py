import os
import requests
import logging

log = logging.getLogger(__name__)

# celery
from celery import shared_task


class LoopsClient:
    # Constructor
    def __init__(self):
        self.api_key = os.getenv("LOOPS_API_KEY", "")
        if not self.api_key:
            raise ValueError("Loops API key not set")

    # ---------------------------------------------------------------------------- #
    #                             TRANSACTIONAL EMAILS                             #
    # ---------------------------------------------------------------------------- #
    def send_transactional_email(
        self,
        transactional_id: str,
        email: str,
        data_variables: dict = {},
    ) -> bool:
        """
        https://loops.so/docs/transactional
        Sends a transactional email using a template with transactional_id

        Args:
            transactional_id (str): The id of the transactional email template
            email (str): The email address of the recipient
            data_variables (dict): The data variables to be used in the email template

        # Returns:
        #     bool: True if the email was sent successfully, False otherwise
        """
        endpoint = "https://app.loops.so/api/v1/transactional"

        payload = {
            "transactionalId": transactional_id,
            "email": email,
            "dataVariables": data_variables,
        }

        try:
            response = requests.post(
                endpoint,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )

            # Parse the response's success
            # {'success': False}
            success = response.json().get("success", False)

            if success:
                log.info(f"Transactional email sent to {email}")
            else:
                log.error(f"Error sending transactional email to {email}")
                log.error(response.json())

            return success
        except requests.exceptions.RequestException as e:
            log.error(f"Error sending transactional email to {email}")
            log.error(e)
            return False

    def create_contact(
        self,
        email: str,
        firstName: str | None = None,
        lastName: str | None = None,
        source: str = "app",
        subscribed: bool = True,
        userGroup: str | None = None,
        userId: str | None = None,
        mailingList: dict = {},
        tenantId: str | None = None,
    ):
        """
        https://loops.so/docs/api-reference/create-contact
        Creates a new contact in Loops

        Args:
            See https://loops.so/docs/api-reference/create-contact#request
        """
        endpoint = "https://app.loops.so/api/v1/contacts/create"

        payload = {
            "email": email,
            "firstName": firstName,
            "lastName": lastName,
            "source": source,
            "subscribed": subscribed,
            "userGroup": userGroup,
            "userId": userId,
            "mailingList": mailingList,
            "tenantId": tenantId,
        }

        try:
            response = requests.post(
                endpoint,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )

            log.debug(response.json())

            return response
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def update_or_create_contact(
        self,
        email: str,
        firstName: str | None = None,
        lastName: str | None = None,
        source: str = "app",
        subscribed: bool = True,
        userGroup: str | None = None,
        userId: str | None = None,
        mailingList: dict = {},
        tenantId: str | None = None,
    ):
        """
        https://loops.so/docs/api-reference/update-contact
        Updates a contact in Loops

        Args:
            See https://loops.so/docs/api-reference/update-contact
        """
        endpoint = "https://app.loops.so/api/v1/contacts/update"

        payload = {
            "email": email,
            "firstName": firstName,
            "lastName": lastName,
            "source": source,
            "subscribed": subscribed,
            "userGroup": userGroup,
            "userId": userId,
            "mailingList": mailingList,
            "tenantId": tenantId,
        }

        try:
            response = requests.post(
                endpoint,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )

            log.debug(response.json())

            return response
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}


@shared_task
def send_transactional_email_task(
    transactional_id: str,
    email: str,
    data_variables: dict = {},
) -> bool:
    loops = LoopsClient()
    success = loops.send_transactional_email(transactional_id, email, data_variables)
    return success


@shared_task
def create_contact_task(
    email: str,
    firstName: str,
    lastName: str,
    source: str = "app",
    subscribed: bool = True,
    userGroup: str | None = None,
    userId: str | None = None,
    mailingList: dict = {},
    tenantId: str | None = None,
):
    loops = LoopsClient()
    loops.create_contact(
        email,
        firstName,
        lastName,
        source,
        subscribed,
        userGroup,
        userId,
        mailingList,
        tenantId,
    )


@shared_task
def update_or_create_contact_task(
    email: str,
    firstName: str,
    lastName: str,
    source: str = "app",
    subscribed: bool = True,
    userGroup: str | None = None,
    userId: str | None = None,
    mailingList: dict = {},
    tenantId: str | None = None,
):
    loops = LoopsClient()
    loops.update_or_create_contact(
        email,
        firstName,
        lastName,
        source,
        subscribed,
        userGroup,
        userId,
        mailingList,
        tenantId,
    )
