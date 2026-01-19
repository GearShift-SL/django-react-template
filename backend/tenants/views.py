# django
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view

# Django Rest Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

# Local App
from .models import Invitation, TenantLogo, TenantUser
from .permissions import IsOwnerOrAdmin
from .serializers import (
    InvitationSerializer,
    TenantLogoSerializer,
    TenantSerializer,
    TenantUserListSerializer,
    TenantUserUpdateSerializer,
)
from .mixins import TenantAwareMixin
from .tasks import send_invitation_email_task

# Authentication app
from authentication.models import User


@extend_schema_view(me=extend_schema(tags=["Tenant Info"]))
class TenantInfoView(APIView):
    """
    API View for managing the current user's tenant information.
    GET/PATCH /tenants/info/
    """

    parser_classes = [JSONParser]

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [IsAuthenticated]
        else:
            """
            Only owners and admins can update the tenant information.
            """
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    @extend_schema(
        tags=["Tenant Info"],
        operation_id="tenant_get",
        summary="Get tenant information",
        description="Retrieve the current user's tenant information. Logo field is read-only here. Use /tenant/logo/ for logo uploads.",
        responses={
            200: TenantSerializer,
        },
    )
    def get(self, request):
        """
        GET /tenants/info/

        Retrieves tenant data in JSON format. Logo field is read-only here.
        Use the logo endpoint for logo uploads.
        """
        tenant = request.user.tenant_user.tenant
        serializer = TenantSerializer(tenant, context={"request": request})
        return Response(serializer.data)

    @extend_schema(
        tags=["Tenant Info"],
        operation_id="tenant_update",
        summary="Update tenant information",
        description="Update the current user's tenant information. Logo field is read-only here. Use /tenant/logo/ for logo uploads.",
        request=TenantSerializer,
        responses={
            200: TenantSerializer,
        },
    )
    def patch(self, request):
        """
        PATCH /tenants/info/

        Updates tenant data in JSON format. Logo field is read-only here.
        Use the logo endpoint for logo uploads.
        """
        tenant = request.user.tenant_user.tenant
        serializer = TenantSerializer(
            tenant, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TenantLogoView(APIView):
    """
    API View for managing the current user's tenant logo.
    PUT/DELETE /tenants/info/logo/
    """

    parser_classes = [MultiPartParser]

    def get_permissions(self):
        permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    @extend_schema(
        tags=["Tenant Info"],
        operation_id="tenant_logo_upload",
        summary="Upload or replace tenant logo",
        description="Upload or replace the tenant's logo. Expects multipart/form-data.",
        request=TenantLogoSerializer,
        responses={
            200: TenantLogoSerializer,
        },
    )
    def put(self, request):
        """
        PUT /tenants/info/logo/

        Upload or replace tenant logo. Expects multipart/form-data.
        """
        tenant = request.user.tenant_user.tenant

        # Get or create the logo object
        logo, created = TenantLogo.objects.get_or_create(tenant=tenant)

        # If updating, delete the old image file
        if not created and logo.image:
            logo.image.delete(save=False)

        serializer = TenantLogoSerializer(
            logo, data=request.data, partial=False, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Tenant Info"],
        operation_id="tenant_logo_delete",
        summary="Delete tenant logo",
        description="Delete the tenant's logo.",
        responses={
            200: OpenApiResponse(
                description="Logo deleted successfully.",
            ),
        },
    )
    def delete(self, request):
        """
        DELETE /tenant/logo/

        Delete the tenant logo.
        """
        tenant = request.user.tenant_user.tenant

        try:
            logo = TenantLogo.objects.get(tenant=tenant)
            # Delete the image file
            if logo.image:
                logo.image.delete(save=False)
            logo.delete()
            return Response(
                {"detail": "Logo deleted successfully."}, status=status.HTTP_200_OK
            )
        except TenantLogo.DoesNotExist:
            return Response(
                {"detail": "No logo found to delete."}, status=status.HTTP_404_NOT_FOUND
            )


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

        # Delete the underlying user object (this will cascade delete the TenantUser)
        user = instance.user
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if a user with this email already exists
        email = serializer.validated_data.get("email")
        if User.objects.filter(email=email).exists():
            return Response(
                {"detail": _("A user with this email already exists.")},
                status=status.HTTP_409_CONFLICT,
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

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
