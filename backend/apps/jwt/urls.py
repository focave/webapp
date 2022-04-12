from django.urls import path

from .views import (
    CookieTokenDeleteView,
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    CookieTokenVerifyView,
)

urlpatterns = [
    path("", CookieTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("delete/", CookieTokenDeleteView.as_view(), name="token_delete"),
    path("refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", CookieTokenVerifyView.as_view(), name="token_verify"),
]

handler400 = "apps.jwt.exceptions.bad_request"
