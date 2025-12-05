from rest_framework import serializers

from tenants.serializers import SimpleTenantSerializer, TenantUserSimpleSerializer

from .models import User, UserProfile


class StartAuthRequestSerializer(serializers.Serializer):
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
    code = serializers.CharField()  # length per your OTP (e.g., max_length=6/8)


class CodeConfirmResponseSerializer(serializers.Serializer):
    # Tweak to match what Allauth returns in your setup (user, tokens, etc.)
    user = serializers.DictField()
    # access = serializers.CharField(required=False)
    # refresh = serializers.CharField(required=False)


class CodeConfirmErrorSerializer(serializers.Serializer):
    code = serializers.CharField()
    detail = serializers.CharField()


class ProviderTokenRequestSerializer(serializers.Serializer):
    provider = serializers.CharField()  # e.g. "google"
    process = serializers.ChoiceField(choices=["login", "connect"])
    token = (
        serializers.DictField()
    )  # e.g. {"id_token": "..."} or {"access_token": "..."}


class ProviderTokenResponseSerializer(serializers.Serializer):
    user = serializers.DictField()
    # access = serializers.CharField(required=False)
    # refresh = serializers.CharField(required=False)


class ProviderTokenErrorSerializer(serializers.Serializer):
    code = serializers.CharField()
    detail = serializers.CharField()


class ProviderSerializer(serializers.Serializer):
    provider = serializers.CharField()
    client_id = serializers.CharField(allow_blank=True, required=False)


class ProvidersListResponseSerializer(serializers.Serializer):
    providers = ProviderSerializer(many=True)


class SessionStatusResponseSerializer(serializers.Serializer):
    # adapt to your response (many setups include user info)
    user = serializers.DictField(required=False)
    is_authenticated = serializers.BooleanField(required=False)


class SessionStatusErrorSerializer(serializers.Serializer):
    code = serializers.CharField()
    detail = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["avatar"]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["pk", "email", "first_name", "last_name", "profile"]
        read_only_fields = ["pk", "email", "profile"]


class UserMeSerializer(serializers.ModelSerializer):
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
