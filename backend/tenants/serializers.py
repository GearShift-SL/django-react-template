# django REST framework
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

# Local App
from .models import Invitation, Tenant, TenantLogo, TenantUser


# ---------------------------------------------------------------------------- #
#                                  TENANT USER                                 #
# ---------------------------------------------------------------------------- #
class TenantUserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantUser
        fields = [
            "pk",
            "role",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class TenantUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantUser
        fields = [
            "pk",
            "role",
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

    class Meta:
        model = Tenant
        fields = [
            "pk",
            "name",
            "slug",
            "logo",
            "website",
            "tenant_users",
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
        # Filter out tenant users linked to superusers using a single efficient query
        tenant_users = obj.tenant_users.select_related("user").filter(
            user__is_superuser=False
        )
        return TenantUserListSerializer(tenant_users, many=True).data


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
            "code",
            "is_accepted",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "tenant",
            "invited_by",
            "code",
            "is_accepted",
            "created_at",
            "updated_at",
        ]
