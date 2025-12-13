# Django Rest Framework
from rest_framework import serializers

# Tenants App
from tenants.serializers import SimpleTenantSerializer, TenantUserSimpleSerializer

# Local App
from .models import User, UserProfile


# ============================================================================
# Authentication Flow Serializers
# ============================================================================


class StartAuthRequestSerializer(serializers.Serializer):
    """
    Request serializer for starting authentication flow (login or signup).
    """
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)

    def validate(self, attrs):
        if bool(attrs.get("email")) == bool(attrs.get("phone")):
            raise serializers.ValidationError(
                "Provide exactly one of 'email' or 'phone'."
            )
        return attrs


class StartAuthResponseSerializer(serializers.Serializer):
    """
    Shape this to reflect your actual auth success payload (user, tokens, etc.).
    This is only for documentation; the real response comes from Allauth.
    """

    user = serializers.DictField()
    # access = serializers.CharField(required=False)
    # refresh = serializers.CharField(required=False)


class StartAuthErrorSerializer(serializers.Serializer):
    code = serializers.CharField()
    detail = serializers.CharField()


class CodeConfirmRequestSerializer(serializers.Serializer):
    """
    Request serializer for confirming login code.
    """

    code = serializers.CharField()


class CodeConfirmResponseSerializer(serializers.Serializer):
    """
    Response serializer for successful code confirmation.
    """

    user = serializers.DictField()


class CodeConfirmErrorSerializer(serializers.Serializer):
    """
    Error serializer for code confirmation failures.
    """

    code = serializers.CharField()
    detail = serializers.CharField()


class ProviderTokenRequestSerializer(serializers.Serializer):
    """
    Request serializer for social provider authentication.
    """

    provider = serializers.CharField()
    process = serializers.ChoiceField(choices=["login", "connect"])
    token = serializers.DictField()


class ProviderTokenResponseSerializer(serializers.Serializer):
    """
    Response serializer for successful provider authentication.
    """

    user = serializers.DictField()


class ProviderTokenErrorSerializer(serializers.Serializer):
    """
    Error serializer for provider authentication failures.
    """

    code = serializers.CharField()
    detail = serializers.CharField()


class ProviderSerializer(serializers.Serializer):
    """
    Serializer for social provider information.
    """

    provider = serializers.CharField()
    client_id = serializers.CharField(allow_blank=True, required=False)


class ProvidersListResponseSerializer(serializers.Serializer):
    """
    Response serializer for listing available social providers.
    """

    providers = ProviderSerializer(many=True)


class SessionStatusResponseSerializer(serializers.Serializer):
    """
    Response serializer for session status information.
    """

    user = serializers.DictField(required=False)
    is_authenticated = serializers.BooleanField(required=False)


class SessionStatusErrorSerializer(serializers.Serializer):
    """
    Error serializer for session status failures.
    """

    code = serializers.CharField()
    detail = serializers.CharField()


# ============================================================================
# User and Profile Serializers
# ============================================================================


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile data (avatar, etc.).
    """
    class Meta:
        model = UserProfile
        fields = ["avatar"]


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for basic user information.
    """

    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["pk", "email", "first_name", "last_name", "profile"]
        read_only_fields = ["pk", "email", "profile"]


class UserMeSerializer(serializers.ModelSerializer):
    """
    Serializer for current authenticated user with tenant information.
    """

    tenant = SimpleTenantSerializer(read_only=True)
    tenant_user = TenantUserSimpleSerializer(read_only=True)
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "pk",
            "email",
            "first_name",
            "last_name",
            "tenant",
            "tenant_user",
            "profile",
        ]
        read_only_fields = ["pk", "email", "tenant", "tenant_user", "profile"]
