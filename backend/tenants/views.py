# django
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema

# Django Rest Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

# Local App
from .models import Invitation, Tenant, TenantLogo, TenantUser
from .permissions import IsOwnerOrAdmin
from .serializers import (
    InvitationSerializer,
    TenantLogoSerializer,
    TenantSerializer,
    TenantUserDetailSerializer,
    TenantUserListSerializer,
    TenantUserUpdateSerializer,
)


class TenantInfoViewset(viewsets.GenericViewSet):
    serializer_class = TenantSerializer

    def get_permissions(self):
        if self.action == "me" and self.request.method == "GET":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get", "put", "patch"])
    def me(self, request):
        tenant = request.user.tenant_user.tenant
        if request.method == "GET":
            serializer = self.get_serializer(tenant)
            return Response(serializer.data)

        serializer = self.get_serializer(
            tenant, data=request.data, partial=request.method == "PATCH"
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


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


class TenantUserViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    List, Retrieve and Update viewset for the TenantUser model.
    """

    queryset = TenantUser.objects.none()  # Empty queryset just for type information

    def get_queryset(self):
        return self.request.user.tenant_user.tenant.tenant_users.all()

    def get_serializer_class(self):
        if self.action == "list":
            return TenantUserListSerializer
        elif self.action == "retrieve" or (
            self.action == "me" and self.request.method == "GET"
        ):
            return TenantUserDetailSerializer
        elif self.action in ["update", "partial_update"] or (
            self.action == "me" and self.request.method in ["PUT", "PATCH"]
        ):
            return TenantUserUpdateSerializer
        return TenantUserDetailSerializer  # Default case

    def get_permissions(self):
        if self.action in ["list", "retrieve"] or (self.action == "me"):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    @extend_schema(responses={200: TenantUserDetailSerializer})
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        # Use update serializer for validation
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        # Use retrieve serializer for response
        retrieve_serializer = TenantUserDetailSerializer(instance)
        return Response(retrieve_serializer.data)

    @extend_schema(responses={200: TenantUserDetailSerializer})
    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    @extend_schema(
        methods=["PUT", "PATCH"], responses={200: TenantUserDetailSerializer}
    )
    @action(detail=False, methods=["get", "put", "patch"])
    def me(self, request):
        tenant_user = request.user.tenant_user
        if request.method == "GET":
            serializer = self.get_serializer(tenant_user)
            return Response(serializer.data)

        # Use update serializer for validation and saving
        update_serializer = self.get_serializer(
            tenant_user, data=request.data, partial=request.method == "PATCH"
        )
        update_serializer.is_valid(raise_exception=True)
        tenant_user = update_serializer.save()

        # Use retrieve serializer for the response
        retrieve_serializer = TenantUserDetailSerializer(tenant_user)
        return Response(retrieve_serializer.data)


class InvitationViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    A viewset that provides the `create` and `list` actions.
    """

    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        return Invitation.objects.for_current_tenant()

    def perform_create(self, serializer):

        # Save the tenant and invited_by fields
        serializer.save(tenant=self.request.user.tenant, invited_by=self.request.user)
