from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.http.response import HttpResponseRedirect
from django.utils.encoding import iri_to_uri
from django.utils.http import url_has_allowed_host_and_scheme
from drf_spectacular.utils import extend_schema
from focave import settings
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainSerializer


class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = []
    authentication_classes = []
    serializer_class = TokenObtainSerializer

    @extend_schema(exclude=True)
    def get(self, request):
        return Response(
            data={
                "serializer": self.serializer_class,
                "next": request.GET.get("next", ""),
            },
            template_name="api/login.html",
        )


class LogoutView(SuccessURLAllowedHostsMixin, APIView):
    permission_classes = []
    authentication_classes = []

    def get_serializer_class(self):
        return None

    @extend_schema(exclude=True)
    def get(self, request):
        redirect_to = request.GET.get("next", "")
        url_is_safe = url_has_allowed_host_and_scheme(
            redirect_to, self.get_success_url_allowed_hosts()
        )
        response = Response()

        if redirect_to and url_is_safe:
            response = HttpResponseRedirect(iri_to_uri(redirect_to))

        response.delete_cookie(key=settings.SIMPLE_JWT["ACCESS_TOKEN_COOKIE_NAME"])
        response.delete_cookie(
            settings.SIMPLE_JWT["REFRESH_TOKEN_COOKIE_NAME"],
            path=settings.SIMPLE_JWT["REFRESH_TOKEN_COOKIE_PATH"],
        )
        response.delete_cookie(key=settings.CSRF_COOKIE_NAME)

        return response
