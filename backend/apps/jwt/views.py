from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.http.response import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.encoding import iri_to_uri
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from focave import settings
from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .serializers import TokenRefreshSerializer, TokenVerifySerializer


def set_refresh_token(response, token):
    response.set_cookie(
        key=settings.SIMPLE_JWT["REFRESH_TOKEN_COOKIE_NAME"],
        value=token,
        expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
        path=settings.SIMPLE_JWT["REFRESH_TOKEN_COOKIE_PATH"],
        domain=settings.SIMPLE_JWT["REFRESH_TOKEN_COOKIE_DOMAIN"],
        secure=settings.SIMPLE_JWT["REFRESH_TOKEN_COOKIE_SECURE"],
        httponly=settings.SIMPLE_JWT["REFRESH_TOKEN_COOKIE_HTTP_ONLY"],
        samesite=settings.SIMPLE_JWT["REFRESH_TOKEN_COOKIE_SAMESITE"],
    )


def set_access_token(response, token):
    response.set_cookie(
        key=settings.SIMPLE_JWT["ACCESS_TOKEN_COOKIE_NAME"],
        value=token,
        expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
        path=settings.SIMPLE_JWT["ACCESS_TOKEN_COOKIE_PATH"],
        domain=settings.SIMPLE_JWT["ACCESS_TOKEN_COOKIE_DOMAIN"],
        secure=settings.SIMPLE_JWT["ACCESS_TOKEN_COOKIE_SECURE"],
        httponly=settings.SIMPLE_JWT["ACCESS_TOKEN_COOKIE_HTTP_ONLY"],
        samesite=settings.SIMPLE_JWT["ACCESS_TOKEN_COOKIE_SAMESITE"],
    )


class CookieTokenObtainPairView(SuccessURLAllowedHostsMixin, TokenObtainPairView):
    """
    Takes a set of user credentials\n
    Sets an access and refresh JSON web token cookie pair, and ensures csrftoken cookie.
    """

    @extend_schema(
        summary="Set tokens in cookies",
        request=TokenObtainSerializer,
        responses={
            200: OpenApiResponse(
                description="Refresh token valid",
            ),
            400: OpenApiResponse(
                description="Bad request",
            ),
        },
    )
    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.pop("refresh")
        access_token = response.data.pop("access")

        redirect_to = request.POST.get("next", "")
        url_is_safe = url_has_allowed_host_and_scheme(
            redirect_to, self.get_success_url_allowed_hosts()
        )
        if redirect_to and url_is_safe:
            response = HttpResponseRedirect(iri_to_uri(redirect_to))

        set_refresh_token(response, refresh_token)
        set_access_token(response, access_token)

        return response


class CookieTokenRefreshView(TokenRefreshView):
    """
    Takes a refresh type JSON web token and sets an access type JSON web
    token cookie if the refresh token is valid.
    """

    serializer_class = TokenRefreshSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Refresh token",
        parameters=[
            OpenApiParameter(
                name=settings.SIMPLE_JWT["REFRESH_TOKEN_COOKIE_NAME"],
                location=OpenApiParameter.COOKIE,
                type=OpenApiTypes.STR,
                required=True,
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Refresh token valid",
            ),
            400: OpenApiResponse(
                description="Bad request",
            ),
            403: OpenApiResponse(
                description="Forbidden",
            ),
        },
    )
    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        request.data.update(request.COOKIES)
        response = super().post(request, *args, **kwargs)
        access_token = response.data.pop(
            settings.SIMPLE_JWT["ACCESS_TOKEN_COOKIE_NAME"]
        )
        set_access_token(response, access_token)

        return response


class CookieTokenVerifyView(TokenVerifyView):
    """
    Takes a token and indicates if it is valid.  This view provides no
    information about a token's fitness for a particular use.
    """

    serializer_class = TokenVerifySerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Verify token",
        parameters=[
            OpenApiParameter(
                name=settings.SIMPLE_JWT["ACCESS_TOKEN_COOKIE_NAME"],
                location=OpenApiParameter.COOKIE,
                type=OpenApiTypes.STR,
                required=True,
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Access token valid",
            ),
            400: OpenApiResponse(
                description="Bad request",
            ),
            403: OpenApiResponse(
                description="Forbidden",
            ),
        },
    )
    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        request.data.update(request.COOKIES)
        response = super().post(request, *args, **kwargs)

        return response


class CookieTokenDeleteView(views.APIView):
    """
    Deletes refresh and access JSON web token cookies.
    """

    serializer_class = None
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        summary="Delete tokens from cookies",
        responses={
            200: OpenApiResponse(
                description="OK",
            ),
            400: OpenApiResponse(
                description="Bad request",
            ),
            403: OpenApiResponse(
                description="Forbidden",
            ),
        },
    )
    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        response = Response(data={}, status=status.HTTP_200_OK)

        response.delete_cookie(settings.SIMPLE_JWT["ACCESS_TOKEN_COOKIE_NAME"])
        response.delete_cookie(
            settings.SIMPLE_JWT["REFRESH_TOKEN_COOKIE_NAME"],
            path=settings.SIMPLE_JWT["REFRESH_TOKEN_COOKIE_PATH"],
        )
        response.delete_cookie(settings.CSRF_COOKIE_NAME)

        return response
