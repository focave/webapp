import logging

from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action

from apps.jwt.authentication import CSRFEnforcedJWTCookieAuthentication

from .permissions import CustomObjectPermissions
from .serializers import UserSerializer

logger = logging.Logger(__name__)


class UserViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    filterset_fields = ("id", "email", "last_login", "date_joined")

    def get_authenticators(self):
        """
        Instantiates and returns the list of authenticators that this view requires.
        """
        # if self.request.method == "POST":
        if self.request is not None and self.request.method == "POST":
            authentication_classes = []
        else:
            authentication_classes = [CSRFEnforcedJWTCookieAuthentication]
        return [auth() for auth in authentication_classes]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "list":
            permission_classes = [permissions.IsAdminUser]
        elif self.action == "create":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [CustomObjectPermissions]

        return [permission() for permission in permission_classes]

    @extend_schema(
        summary="List users",
        responses={
            200: OpenApiResponse(description="OK", response=UserSerializer),
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
        },
    )
    def list(self, request, *args, **kwargs):
        """
        Lists all users \n
        Available only for admins.
        """
        return super().list(request)

    @extend_schema(
        summary="Create user",
        responses={
            201: OpenApiResponse(description="Created", response=UserSerializer),
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
        },
    )
    @method_decorator(csrf_exempt)
    def create(self, request, *args, **kwargs):
        """
        Creates a user from given data.
        """
        return super().create(request)

    @extend_schema(
        summary="Retrieve user by id",
        responses={
            200: OpenApiResponse(description="OK", response=UserSerializer),
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
        },
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Retrieves user with given id.
        """
        return super().retrieve(request, pk=pk, *args, **kwargs)

    @extend_schema(
        summary="Update user by id",
        responses={
            200: OpenApiResponse(description="OK", response=UserSerializer),
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
        },
    )
    def update(self, request, pk=None, *args, **kwargs):
        """
        Updates user with given id.
        """
        return super().update(request, pk=pk, *args, **kwargs)

    @extend_schema(
        summary="Partially update user by id",
        responses={
            200: OpenApiResponse(description="OK", response=UserSerializer),
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
        },
    )
    def partial_update(self, request, pk=None, *args, **kwargs):
        """
        Partially updates user with given id.
        """
        return super().partial_update(request, pk=pk, *args, **kwargs)

    @extend_schema(
        summary="Destroy user by id",
        responses={
            204: OpenApiResponse(description="No Content"),
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
        },
    )
    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Destroy user with given id.
        """
        return super().destroy(request, pk=pk, *args, **kwargs)

    @extend_schema(
        summary="Retrieve current user",
        responses={
            200: OpenApiResponse(description="OK", response=UserSerializer),
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
        },
    )
    @action(["get"], detail=False)
    def me(self, request, pk=None, *args, **kwargs):
        """
        Retrieve currently logged in user.
        """
        self.kwargs["pk"] = request.user.id
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update current user",
        responses={
            200: OpenApiResponse(description="OK", response=UserSerializer),
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
        },
    )
    @me.mapping.put
    def me_update(self, request, pk=None, *args, **kwargs):
        """
        Update currently logged in user.
        """
        self.kwargs["pk"] = request.user.id
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update current user",
        responses={
            200: OpenApiResponse(description="OK", response=UserSerializer),
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
        },
    )
    @me.mapping.patch
    def me_partial_update(self, request, pk=None, *args, **kwargs):
        """
        Partially update currently logged in user.
        """
        self.kwargs["pk"] = request.user.id
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Destroy current user",
        responses={
            204: OpenApiResponse(description="No Content"),
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
        },
    )
    @me.mapping.delete
    def me_destroy(self, request, pk=None, *args, **kwargs):
        """
        Destroy currently logged in user.
        """
        self.kwargs["pk"] = request.user.id
        return self.destroy(request, *args, **kwargs)
