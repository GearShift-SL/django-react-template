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
    path("me/", TenantInfoView.as_view(), name="tenant-me"),
    path("me/logo/", TenantLogoView.as_view(), name="tenant-logo"),
]

urlpatterns += router.urls
