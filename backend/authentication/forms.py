from django import forms
from django.utils.translation import gettext_lazy as _
from tenants.models import Tenant, TenantUser


class CustomSignupForm(forms.Form):
    # email = forms.EmailField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "type": "email",
    #             "placeholder": _("Email address"),
    #             "autocomplete": "email",
    #         }
    #     )
    # )

    # Uncomment this if you want to prompt for a first name
    # first_name = forms.CharField(
    #     label=_("First Name"),
    #     widget=forms.TextInput(
    #         attrs={"placeholder": _("First Name"), "autocomplete": "first-name"}
    #     ),
    # )

    # Uncomment this if you want to prompt for a team name
    # team_name = forms.CharField(
    #     label=_("Team Name"),
    #     widget=forms.TextInput(
    #         attrs={"placeholder": _("Team Name"), "autocomplete": "team-name"}
    #     ),
    # )

    def signup(self, request, user):
        """
        Invoked at signup time to complete the signup of the user.
        """

        # Create the tenant and the tenant user when a new user signs up
        try:
            # Build the tenant name
            tenant_name = f"{self.cleaned_data['first_name']}'s Team"

            # Create the tenant
            tenant = Tenant.objects.create(name=tenant_name)

            # Create the tenant user with the owner role
            TenantUser.objects.create(tenant=tenant, user=user, role="owner")
        except Exception as e:
            raise forms.ValidationError(_("Error creating tenant"))
