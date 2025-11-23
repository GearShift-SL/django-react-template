from rest_framework.exceptions import PermissionDenied


class TenantAwareMixin:
    def get_queryset(self):
        # Filter queryset by the user's tenant
        # IMPORTANT: If this function is overridden, this method needs to be called like this:
        # queryset = super().get_queryset()  # This applies tenant filtering
        # Then do whatever you need with the queryset
        return (
            super().get_queryset().filter(tenant=self.request.user.tenant_user.tenant)
        )

    def perform_create(self, serializer):
        # Set the tenant automatically on create
        # IMPORTANT: If this function is overridden, the tenant must be set manually
        serializer.save(tenant=self.request.user.tenant_user.tenant)

    def perform_update(self, serializer):
        # Prevent tenant changes
        # IMPORTANT: If this function is overridden, the tenant must be set manually
        if serializer.instance.tenant != self.request.user.tenant_user.tenant:
            raise PermissionDenied("You cannot change the tenant of this object")
        serializer.save()
