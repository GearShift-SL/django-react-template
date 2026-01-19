# Rest Framework
from rest_framework.routers import DefaultRouter
from django.urls import path

# Local App
from .views import (
    InvitationViewSet,
    TenantInfoView,
    TenantLogoView,
    TenantUserViewSet,
)


router = DefaultRouter()

router.register(r"invitations", InvitationViewSet, basename="invitations")
router.register(r"tenant-users", TenantUserViewSet, basename="tenant-users")


urlpatterns = [
    path("info/", TenantInfoView.as_view(), name="tenant-info"),
    path("info/logo/", TenantLogoView.as_view(), name="tenant-info-logo"),
]

urlpatterns += router.urls
