# django REST framework
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from django.conf import settings

# Local App
from .models import Invitation, Tenant, TenantLogo, TenantUser


# ---------------------------------------------------------------------------- #
#                                  TENANT USER                                 #
# ---------------------------------------------------------------------------- #
class TenantUserListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = TenantUser
        fields = [
            "pk",
            "role",
            "email",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class TenantUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantUser
        fields = [
            "role",
        ]


class TenantUserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantUser
        fields = ["pk", "role"]


# ---------------------------------------------------------------------------- #
#                              TENANT SERIALIZERS                              #
# ---------------------------------------------------------------------------- #
class SimpleTenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ["pk", "name", "slug"]


class TenantSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(required=False, source="logo.image")
    tenant_users = serializers.SerializerMethodField()
    tenants_enabled = serializers.SerializerMethodField()
    me = serializers.SerializerMethodField()

    class Meta:
        model = Tenant
        fields = [
            "pk",
            "name",
            "slug",
            "logo",
            "website",
            "tenant_users",
            "tenants_enabled",
            "me",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "slug",
            "created_at",
            "updated_at",
        ]

    @extend_schema_field(TenantUserListSerializer(many=True))
    def get_tenant_users(self, obj):
        # Filter out tenant users linked to superusers
        tenant_users = obj.tenant_users.select_related("user").filter(
            user__is_superuser=False
        )
        return TenantUserListSerializer(tenant_users, many=True).data

    @extend_schema_field(serializers.BooleanField())
    def get_tenants_enabled(self, obj):
        return settings.ENABLE_TENANTS

    @extend_schema_field(TenantUserSimpleSerializer())
    def get_me(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            tenant_user = obj.tenant_users.filter(user=request.user).first()
            if tenant_user:
                return TenantUserSimpleSerializer(tenant_user).data
        return None


class TenantLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantLogo
        fields = [
            "image",
            "created_at",
        ]
        read_only_fields = [
            "created_at",
        ]


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = [
            "email",
            "invited_by",
            "last_sent_at",
            "accepted_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "tenant",
            "invited_by",
            "last_sent_at",
            "accepted_at",
            "created_at",
            "updated_at",
        ]
