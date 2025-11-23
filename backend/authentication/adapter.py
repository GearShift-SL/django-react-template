# django
from django.conf import settings

# allauth
from allauth.account.adapter import DefaultAccountAdapter
from allauth.headless.adapter import DefaultHeadlessAdapter

# Utils
from utils.loops import send_transactional_email_task

import logging

log = logging.getLogger(__name__)


# Custom Account Adapter to send auth emails to the user
class CustomAccountAdapter(DefaultAccountAdapter):

    def send_mail(self, template_prefix, email, context):
        """
        Send an email to the user

        Args:
            template_prefix (str): The prefix of the email template
            email (str): The email address of the user
            context (dict): The context to be used in the email template. Its structure is defined for every case below
        """

        log.info(f"Sending email to {email} with template {template_prefix}")
        log.debug(f"Context: {context}")

        # ------------------------- Email confirmation signup ------------------------ #
        """
        Context structure if verify by link:
        {
            "user": User object,
            "activate_url": activate_url,
            "key": key,
        }

        or if verify by code:
        {
            'user': <User: test3@mail.daniel.es>,
            'code': 'WJ99YV'
        }
        """
        if "email_confirmation" in template_prefix:

            if "key" in context:
                # Build the email context
                # http://app.autovisita.es/verify-email?key=3b4b4
                FRONTEND_BASE_URL = settings.FRONTEND_BASE_URL
                email_context = {}
                email_context["ACTIVATE_URL"] = (
                    f"{FRONTEND_BASE_URL}/verify-email?key={context['key']}"
                )

                # Set the template ID
                # template_id = SENDGRID_VERIFY_EMAIL_TEMPLATE_ID
                transactional_id = settings.LOOPS_VERIFY_EMAIL_TRANSACTIONAL_ID
            if "code" in context:
                # Build the email context
                email_context = {}
                email_context["VERIFICATION_CODE"] = context["code"]

                # Set the template ID
                # template_id = SENDGRID_VERIFY_EMAIL_TEMPLATE_ID
                transactional_id = settings.LOOPS_VERIFY_EMAIL_TRANSACTIONAL_ID

        # ---------------------------- Login Code Request ---------------------------- #
        """
        Template Prefix: account/email/login_code

        Context structure:
        {
            'code': 'YCSWTC'
        }
        """
        if "login_code" in template_prefix:
            # Build the email context
            email_context = {}
            email_context["LOGIN_CODE"] = context["code"]

            # Set the template ID
            # template_id = SENDGRID_LOGIN_CODE_TEMPLATE_ID
            transactional_id = settings.LOOPS_LOGIN_CODE_TRANSACTIONAL_ID

        # ------------------------------ Send the email ------------------------------ #
        if not transactional_id:
            raise ValueError("Transactional ID not set")

        send_transactional_email_task.delay(
            transactional_id=transactional_id,
            email=email,
            data_variables=email_context,
        )

    # def is_login_by_code_required(self, login) -> bool:
    #     """
    #     Override to ensure social logins never trigger login-by-code.

    #     Keeps default semantics for all other methods.
    #     """
    #     # Import lazily to avoid import-time side effects
    #     from allauth.account import app_settings as allauth_app_settings
    #     from allauth.account import authentication

    #     records = authentication.get_authentication_records(self.request) or []
    #     methods = [rec.get("method") for rec in records if isinstance(rec, dict)]

    #     # If already in a code flow, do not require again
    #     if "code" in methods:
    #         return False

    #     # Never require code for social logins
    #     if "socialaccount" in methods:
    #         log.debug("Bypassing login-by-code for social login. methods=%s", methods)
    #         return False

    #     value = allauth_app_settings.LOGIN_BY_CODE_REQUIRED
    #     if isinstance(value, bool):
    #         return value
    #     if not value:
    #         return False

    #     # Default behavior: require when method is unknown (None) or in configured list
    #     last_method = methods[-1] if methods else None
    #     return last_method is None or last_method in value

    def is_login_by_code_required(self, login) -> bool:
        """
        Returns whether or not login-by-code is required for the given
        login.
        """
        from allauth.account import authentication
        from allauth.account import app_settings

        # log.debug(f"path: {self.request.path}")
        # Possible request paths:
        # /_allauth/browser/v1/auth/signup - Normal signup
        # /_allauth/browser/v1/auth/provider/token - Provider signup and login

        # Get the authentication method from the records
        method = None
        records = authentication.get_authentication_records(self.request)
        if records:
            method = records[-1]["method"]
        if method == "code":
            return False
        value = app_settings.LOGIN_BY_CODE_REQUIRED
        if isinstance(value, bool):
            return value
        if not value:
            return False
        # If the request path is the proviider token endpoint and login
        # by code is not required in social accounts, do not require login-by-code
        if (
            not records
            and "socialaccount" not in value
            and self.request
            and "/provider/token" in self.request.path
        ):
            log.debug("Bypassing login-by-code for provider signup")
            return False

        return method is None or method in value


# Custom Allauth Headless Adapter to include first name in the user data
class CustomHeadlessAdapter(DefaultHeadlessAdapter):

    def serialize_user(self, user):
        """
        Returns the basic user data. Note that this data is also exposed in
        partly authenticated scenario's (e.g. password reset, email
        verification).

        Modified the serializer to include first name
        """
        ret = {
            "id": user.pk,
            "display": user.get_full_name(),
            "has_usable_password": user.has_usable_password(),
        }
        email = user.email
        if email:
            ret["email"] = email
        return ret
