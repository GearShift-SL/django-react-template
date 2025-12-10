# django
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view

# Django Rest Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

# Local App
from .models import Invitation, TenantLogo, TenantUser
from .tasks import send_invitation_email_task
from .permissions import IsOwnerOrAdmin
from .serializers import (
    InvitationSerializer,
    TenantLogoSerializer,
    TenantSerializer,
    TenantUserListSerializer,
    TenantUserUpdateSerializer,
)
from .mixins import TenantAwareMixin


@extend_schema_view(me=extend_schema(tags=["Tenant Info"]))
class TenantInfoViewset(viewsets.GenericViewSet):
    serializer_class = TenantSerializer

    def get_permissions(self):
        if self.action == "me" and self.request.method == "GET":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get", "put"])
    def me(self, request):
        tenant = request.user.tenant_user.tenant
        if request.method == "GET":
            serializer = self.get_serializer(tenant)
            return Response(serializer.data)

        serializer = self.get_serializer(tenant, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@extend_schema_view(
    get=extend_schema(tags=["Tenant Logo"]),
    post=extend_schema(tags=["Tenant Logo"]),
    delete=extend_schema(tags=["Tenant Logo"]),
)
class TenantLogoView(GenericAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = TenantLogoSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def get_object(self):
        try:
            return TenantLogo.objects.get(tenant=self.request.user.tenant_user.tenant)
        except TenantLogo.DoesNotExist:
            return None

    def get(self, request):
        instance = self.get_object()
        if not instance:
            return Response(
                {"detail": "No logo found for this tenant."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = TenantLogoSerializer(instance)
        return Response(serializer.data)

    def post(self, request):
        existing_logo = self.get_object()
        if existing_logo:
            existing_logo.delete()

        serializer = TenantLogoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(tenant=request.user.tenant_user.tenant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        instance = self.get_object()
        if not instance:
            return Response(
                {"detail": "No logo found to delete."}, status=status.HTTP_404_NOT_FOUND
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    list=extend_schema(tags=["Tenant Users"]),
    update=extend_schema(tags=["Tenant Users"]),
    destroy=extend_schema(tags=["Tenant Users"]),
)
class TenantUserViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    List, Update and Destroy viewset for the TenantUser model.
    """

    queryset = TenantUser.objects.none()  # Empty queryset just for type information
    http_method_names = ["get", "put", "delete", "head", "options"]

    def get_queryset(self):
        return self.request.user.tenant_user.tenant.tenant_users.all()

    def get_serializer_class(self):
        if self.action == "update":
            return TenantUserUpdateSerializer
        return TenantUserListSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        current_user_tenant = request.user.tenant_user
        new_role = request.data.get("role")

        # Prevent changing the owner's role (only owner can transfer ownership)
        if instance.role == "owner" and current_user_tenant.pk != instance.pk:
            return Response(
                {"detail": _("Only the owner can transfer ownership.")},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Only owners can set another user as owner
        if new_role == "owner":
            if current_user_tenant.role != "owner":
                return Response(
                    {"detail": _("Only the owner can set another user as owner.")},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Transfer ownership: set the new user as owner and current owner as admin
            instance.role = "owner"
            instance.save()
            current_user_tenant.role = "admin"
            current_user_tenant.save()

            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        # Prevent owner from changing their own role without transferring ownership
        if instance.role == "owner" and current_user_tenant.pk == instance.pk:
            return Response(
                {
                    "detail": _(
                        "Owner cannot change their role. Transfer ownership to another user first."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Prevent deletion of owners - they must transfer ownership first
        if instance.role == "owner":
            return Response(
                {
                    "detail": _(
                        "Cannot delete the owner. Transfer ownership to another user first."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().destroy(request, *args, **kwargs)


@extend_schema_view(
    create=extend_schema(tags=["Tenant Invitations"]),
    list=extend_schema(tags=["Tenant Invitations"]),
    resend=extend_schema(tags=["Tenant Invitations"]),
)
class InvitationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
    TenantAwareMixin,
):
    """
    A viewset that provides the `create` and `list` actions.
    """

    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.user.tenant_user.tenant, invited_by=self.request.user
        )

    @extend_schema(request=None)
    @action(detail=True, methods=["post"])
    def resend(self, request, pk=None):
        """
        Resend an invitation email.
        Returns 403 if the last invitation was sent less than 24 hours ago.
        """
        invitation = self.get_object()

        # Check if the last invitation was sent less than 24 hours ago
        if invitation.last_sent_at:
            time_since_last_sent = timezone.now() - invitation.last_sent_at
            if time_since_last_sent < timedelta(hours=24):
                return Response(
                    {
                        "detail": _(
                            "Invitation was already sent within the last 24 hours."
                        )
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        # Trigger the celery task to send the invitation email
        send_invitation_email_task.delay(invitation.pk)

        return Response(
            {"detail": _("Invitation email has been queued for resending.")},
            status=status.HTTP_200_OK,
        )
