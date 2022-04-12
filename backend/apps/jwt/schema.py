from drf_spectacular.extensions import OpenApiAuthenticationExtension
from focave import settings

from .authentication import CSRFEnforcedJWTCookieAuthentication


class CSRFEnforcedJWTCookieAuthenticationExtension(OpenApiAuthenticationExtension):
    name = "CSRFEnforcedJWTCookieAuthentication"
    target_class = CSRFEnforcedJWTCookieAuthentication

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "cookie",
            "name": settings.SIMPLE_JWT["ACCESS_TOKEN_COOKIE_NAME"],
        }
