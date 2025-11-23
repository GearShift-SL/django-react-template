from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to only allow users with an owner or an admin role to access it.
    """

    def has_permission(self, request, view):
        if request.user.tenant_user.role.lower() in ["owner", "admin"]:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.tenant_user.role.lower() in ["owner", "admin"]:
            return True
        return False
