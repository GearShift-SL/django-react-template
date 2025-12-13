# django
from django.contrib.auth import get_user_model
import logging
import json

# Django Rest Framework
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

# Allauth
from allauth.headless.account.views import (
    ConfirmLoginCodeView as AllauthConfirmLoginCodeView,
    RequestLoginCodeView as AllauthRequestLoginCodeView,
    SignupView as AllauthSignupView,
    SessionView as AllauthSessionView,
)
from allauth.headless.socialaccount.views import (
    ProviderTokenView as AllauthProviderTokenView,
)

# DRF Spectacular
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)

# Local App
from .serializers import (
    CodeConfirmErrorSerializer,
    CodeConfirmRequestSerializer,
    CodeConfirmResponseSerializer,
    ProviderTokenRequestSerializer,
    ProviderTokenResponseSerializer,
    ProviderTokenErrorSerializer,
    ProvidersListResponseSerializer,
    StartAuthErrorSerializer,
    StartAuthRequestSerializer,
    StartAuthResponseSerializer,
    UserSerializer,
    UserMeSerializer,
    UserProfileSerializer,
    SessionStatusResponseSerializer,
    SessionStatusErrorSerializer,
)
from .models import User, UserProfile

log = logging.getLogger(__name__)


@extend_schema_view(
    post=extend_schema(
        tags=["Authentication Email"],
        operation_id="auth_start",
        parameters=[
            OpenApiParameter(
                name="client",
                location=OpenApiParameter.PATH,
                required=True,
                description="The type of client accessing the API.",
                enum=["app", "browser"],
            ),
        ],
        request=StartAuthRequestSerializer,
        responses={
            200: OpenApiResponse(
                response=StartAuthResponseSerializer,
                description="Auth flow started or completed",
            ),
            400: StartAuthErrorSerializer,
            401: StartAuthErrorSerializer,
            403: StartAuthErrorSerializer,
            409: StartAuthErrorSerializer,
            429: StartAuthErrorSerializer,
        },
        examples=[
            OpenApiExample(
                "Start auth (existing user by email)",
                value={"email": "ada@example.com"},
                request_only=True,
            ),
            OpenApiExample(
                "Start auth (new user by email)",
                value={"email": "newuser@example.com"},
                request_only=True,
            ),
            OpenApiExample(
                "Start auth (existing user by phone)",
                value={"phone": "+34123456789"},
                request_only=True,
            ),
        ],
        summary="Request login code or sign up",
        description=(
            "If the identifier belongs to an existing user, request a one-time login code. "
            "Otherwise, create the user (per your Allauth config) and then proceed."
        ),
    )
)
class StartAuthView(APIView):
    """
    POST /auth/<client>/start

    If a user with the given identifier exists:
        -> delegate to allauth.headless.account.views.RequestLoginCodeView
    Else:
        -> delegate to allauth.headless.account.views.SignupView
    """

    permission_classes = [AllowAny]
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = "auth_start"

    def post(self, request: Request, client: str, *args, **kwargs):
        # Parse JSON without touching DRF's request.data to avoid consuming the stream
        try:
            raw_body = request._request.body or b"{}"
            payload = json.loads(raw_body.decode("utf-8")) if raw_body else {}
        except json.JSONDecodeError:
            return Response({"detail": "Invalid JSON."}, status=400)

        # Validate input (email OR phone)
        data = StartAuthRequestSerializer(data=payload)
        data.is_valid(raise_exception=True)
        email = data.validated_data.get("email")
        phone = data.validated_data.get("phone")

        # Determine existence by your chosen identifier.
        # If you support phone auth, adjust this lookup accordingly.
        User = get_user_model()
        exists = False
        if email:
            exists = User._default_manager.filter(email__iexact=email).exists()
        elif phone:
            # If you store phone normalized (E.164), normalize before lookup.
            exists = User._default_manager.filter(phone=phone).exists()

        if exists:
            # Existing user → request login code
            view = AllauthRequestLoginCodeView.as_api_view(client=client)
            return view(request._request, *args, **kwargs)
        else:
            # New user → signup flow
            view = AllauthSignupView.as_api_view(client=client)
            return view(request._request, *args, **kwargs)


@extend_schema_view(
    post=extend_schema(
        tags=["Authentication Email"],
        operation_id="auth_confirm_code",
        parameters=[
            OpenApiParameter(
                name="client",
                location=OpenApiParameter.PATH,
                required=True,
                description="The type of client accessing the API.",
                enum=["app", "browser"],
            ),
        ],
        request=CodeConfirmRequestSerializer,
        responses={
            200: OpenApiResponse(
                response=CodeConfirmResponseSerializer,
                description="Authenticated by code.",
            ),
            400: CodeConfirmErrorSerializer,
            401: CodeConfirmErrorSerializer,
            409: CodeConfirmErrorSerializer,
            429: CodeConfirmErrorSerializer,
        },
        examples=[
            OpenApiExample(
                "Confirm code",
                value={"code": "123456"},
                request_only=True,
            ),
        ],
        summary="Confirm login code",
        description='Use this endpoint to pass along the received one-time "special" login code.',
    )
)
class ConfirmLoginCodeView(APIView):
    """
    POST /auth/<client>/code/confirm
    Delegates to allauth.headless.account.views.ConfirmLoginCodeView
    """

    permission_classes = [AllowAny]
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = "auth_code_confirm"

    def post(self, request: Request, client: str, *args, **kwargs):
        # validate for docs + early 400s without consuming DRF request.data
        try:
            raw_body = request._request.body or b"{}"
            payload = json.loads(raw_body.decode("utf-8")) if raw_body else {}
        except json.JSONDecodeError:
            return Response({"detail": "Invalid JSON."}, status=400)
        CodeConfirmRequestSerializer(data=payload).is_valid(raise_exception=True)

        # delegate to allauth's FBV created by .as_api_view(client=...)
        allauth_view = AllauthConfirmLoginCodeView.as_api_view(client=client)
        # IMPORTANT: pass the underlying Django HttpRequest so allauth sees the raw request
        return allauth_view(request._request, *args, **kwargs)


@extend_schema_view(
    post=extend_schema(
        tags=["Authentication Provider"],
        operation_id="auth_provider_token",
        parameters=[
            OpenApiParameter(
                name="client",
                location=OpenApiParameter.PATH,
                required=True,
                description="The type of client accessing the API.",
                enum=["app", "browser"],
            ),
            OpenApiParameter(
                name="X-Session-Token",
                location=OpenApiParameter.HEADER,
                required=False,
                description="Session token. Only needed when client is 'app'.",
            ),
        ],
        request=ProviderTokenRequestSerializer,
        responses={
            200: OpenApiResponse(
                response=ProviderTokenResponseSerializer,
                description="The user is authenticated.",
            ),
            400: ProviderTokenErrorSerializer,
            401: ProviderTokenErrorSerializer,
            403: ProviderTokenErrorSerializer,
            429: ProviderTokenErrorSerializer,
        },
        examples=[
            OpenApiExample(
                "Google login (browser)",
                value={
                    "provider": "google",
                    "process": "login",
                    "token": {"id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."},
                },
                request_only=True,
            ),
            OpenApiExample(
                "Google connect (app)",
                value={
                    "provider": "google",
                    "process": "connect",
                    "token": {"access_token": "ya29.a0ARrdaM..."},
                },
                request_only=True,
            ),
        ],
        summary="Provider token",
        description=(
            "Authenticate using a third-party provider token (e.g., Google). "
            "`process=login` logs in (or signs up) the user. `process=connect` links the "
            "provider to the currently authenticated user. For mobile (`client=app`), send "
            "`X-Session-Token` header from the prior app session bootstrap."
        ),
    )
)
class ProviderTokenView(APIView):
    """
    POST /auth/<client>/provider/token

    Delegates 1:1 to allauth.headless.account.views.ProviderTokenView.
    """

    permission_classes = [AllowAny]
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = "auth_provider_token"

    def post(self, request: Request, client: str, *args, **kwargs):
        # Optional: validate so your API returns clean 400s before delegating, without consuming DRF request.data
        try:
            raw_body = request._request.body or b"{}"
            payload = json.loads(raw_body.decode("utf-8")) if raw_body else {}
        except json.JSONDecodeError:
            return Response({"detail": "Invalid JSON."}, status=400)
        ProviderTokenRequestSerializer(data=payload).is_valid(raise_exception=True)

        # Delegate to Allauth’s view created with the client bound in
        allauth_view = AllauthProviderTokenView.as_api_view(client=client)
        # Pass the underlying Django HttpRequest so Allauth handles cookies/headers/session
        return allauth_view(request._request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(
        tags=["Authentication Provider"],
        operation_id="auth_providers_list",
        responses={
            200: OpenApiResponse(
                response=ProvidersListResponseSerializer,
                description="List of available providers and their client IDs.",
            )
        },
        summary="List social providers",
        description="Returns enabled Allauth providers and their client IDs.",
    )
)
class ProvidersListView(APIView):
    """
    GET /auth/providers

    Returns the configured Allauth providers and their client IDs for the current site.
    """

    permission_classes = [AllowAny]

    def get(self, request: Request, *args, **kwargs):
        # Derive providers from settings and installed apps
        from django.conf import settings

        provider_ids = set()
        try:
            cfg = getattr(settings, "SOCIALACCOUNT_PROVIDERS", {})
            if isinstance(cfg, dict):
                provider_ids.update(cfg.keys())
        except Exception:
            pass

        try:
            for app in getattr(settings, "INSTALLED_APPS", []) or []:
                prefix = "allauth.socialaccount.providers."
                if isinstance(app, str) and app.startswith(prefix):
                    provider_ids.add(app[len(prefix) :])
        except Exception:
            pass

        provider_list = []
        for provider_id in sorted(provider_ids):
            client_id = ""
            try:
                app_cfg = settings.SOCIALACCOUNT_PROVIDERS.get(provider_id, {})
                app_cfg_app = (
                    app_cfg.get("APP", {}) if isinstance(app_cfg, dict) else {}
                )
                client_id = app_cfg_app.get("client_id", "")
            except Exception:
                client_id = ""

            provider_list.append({"provider": provider_id, "client_id": client_id})

        serializer = ProvidersListResponseSerializer({"providers": provider_list})
        return Response(serializer.data)


@extend_schema_view(
    get=extend_schema(
        tags=["Authentication Session"],
        operation_id="auth_session_status",
        summary="Get authentication status",
        description="Retrieve information about the authentication status for the current session.",
        parameters=[
            OpenApiParameter(
                name="client",
                location=OpenApiParameter.PATH,
                required=True,
                description="The type of client accessing the API.",
                enum=["app", "browser"],
            ),
            OpenApiParameter(
                name="X-Session-Token",
                location=OpenApiParameter.HEADER,
                required=False,
                description="Only needed when client is 'app'.",
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=SessionStatusResponseSerializer,
                description="The user is authenticated.",
            ),
            401: SessionStatusErrorSerializer,
            410: SessionStatusErrorSerializer,
        },
    ),
    delete=extend_schema(
        tags=["Authentication Session"],
        operation_id="auth_logout",
        summary="Logout",
        description="Logs out the user from the current session.",
        parameters=[
            OpenApiParameter(
                name="client",
                location=OpenApiParameter.PATH,
                required=True,
                description="The type of client accessing the API.",
                enum=["app", "browser"],
            ),
            OpenApiParameter(
                name="X-Session-Token",
                location=OpenApiParameter.HEADER,
                required=False,
                description="Only needed when client is 'app'.",
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=SessionStatusResponseSerializer,
                description="Logged out (or no-op if already logged out).",
            ),
            401: SessionStatusErrorSerializer,
        },
    ),
)
class SessionView(APIView):
    """
    GET/DELETE /auth/<client>/session

    Thin wrapper around allauth.headless.account.views.SessionView.
    """

    permission_classes = [AllowAny]

    def _delegate(self, request: Request, client: str, *args, **kwargs):
        # Delegate to Allauth FBV bound to the client
        view = AllauthSessionView.as_api_view(client=client)
        return view(request._request, *args, **kwargs)

    def get(self, request: Request, client: str, *args, **kwargs):
        return self._delegate(request, client, *args, **kwargs)

    def delete(self, request: Request, client: str, *args, **kwargs):
        return self._delegate(request, client, *args, **kwargs)


@extend_schema_view(me=extend_schema(tags=["Authentication User"]))
class UserViewSet(GenericViewSet):
    """
    ViewSet for managing the current user's profile.
    """

    serializer_class = UserSerializer

    def get_queryset(self):
        # Scope to the current user only
        return User.objects.filter(pk=self.request.user.pk)

    def get_serializer_class(self):
        if getattr(self, "action", None) == "me" and self.request.method == "GET":
            return UserMeSerializer
        return UserSerializer

    @action(detail=False, methods=["get", "patch"])
    def me(self, request):
        if request.method == "GET":
            return Response(self.get_serializer(request.user).data)

        partial = request.method == "PATCH"
        serializer = UserSerializer(request.user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserMeSerializer(request.user).data)


@extend_schema_view(me=extend_schema(tags=["Authentication User Profile"]))
class UserProfileViewSet(GenericViewSet):
    """
    ViewSet for managing the current user's profile avatar and other profile data.
    """

    parser_classes = [MultiPartParser]
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        # Scope to the current user only
        return UserProfile.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if getattr(self, "action", None) == "me" and self.request.method == "GET":
            return UserProfileSerializer
        return UserProfileSerializer

    @action(detail=False, methods=["get", "patch"])
    def me(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)

        if request.method == "GET":
            serializer = UserProfileSerializer(profile, context={"request": request})
            return Response(serializer.data)

        partial = request.method == "PATCH"
        serializer = UserProfileSerializer(
            profile, data=request.data, partial=partial, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
