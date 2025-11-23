from django.urls.resolvers import URLPattern


from django.urls import path

from .views import (
    ConfirmLoginCodeView,
    ProviderTokenView,
    ProvidersListView,
    StartAuthView,
    UserViewSet,
    SessionView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")

urlpatterns: list[URLPattern] = [
    path("<str:client>/start/", StartAuthView.as_view(), name="auth-start"),
    path(
        "providers/",
        ProvidersListView.as_view(),
        name="auth-providers-list",
    ),
    path(
        "<str:client>/code/confirm/",
        ConfirmLoginCodeView.as_view(),
        name="auth-code-confirm",
    ),
    path(
        "<str:client>/provider/token/",
        ProviderTokenView.as_view(),
        name="auth-provider-token",
    ),
    path("<str:client>/session/", SessionView.as_view(), name="auth-session"),
]
urlpatterns += router.urls
