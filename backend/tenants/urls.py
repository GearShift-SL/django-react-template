# Rest Framework
from rest_framework.routers import DefaultRouter
from django.urls import path

# Local App
from .views import (
    InvitationViewSet,
    TenantInfoViewset,
    TenantLogoView,
    TenantUserViewSet,
)


router = DefaultRouter()

router.register(r"invitations", InvitationViewSet, basename="invitations")
router.register(r"tenant", TenantInfoViewset, basename="tenant")
# NOTE: tenant-logo now handled by direct path below
router.register(r"tenant-users", TenantUserViewSet, basename="tenant-users")


urlpatterns = [
    path("tenant-logo/", TenantLogoView.as_view(), name="tenant-logo"),
]

urlpatterns += router.urls
