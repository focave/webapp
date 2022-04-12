"""
Django settings for focave project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import datetime
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-l2z4k$=!7i1(el15=u+=#2&uo)33kc)#%sv-xll1d!ax$hhov9"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# Application definition

INSTALLED_APPS = [
    "apps.jwt",
    "apps.api",
    "apps.docs",
    "apps.users",
    # "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    # "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    # "rest_framework.authtoken",
    "corsheaders",
    "rest_framework_simplejwt",
    "guardian",
    "django_filters",
    "drf_spectacular",
    "crispy_forms",
]


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    # "django.contrib.auth.middleware.AuthenticationMiddleware",
    # "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    "https://127.0.0.1:3000" if not DEBUG else "http://127.0.0.1:3000",
)

ROOT_URLCONF = "focave.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "focave.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ["POSTGRES_HOST"],
        "PORT": os.environ["POSTGRES_PORT"],
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.jwt.authentication.CSRFEnforcedJWTCookieAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(minutes=5),
    "ACCESS_TOKEN_COOKIE_NAME": "access_token",
    "ACCESS_TOKEN_COOKIE_PATH": "/",
    "ACCESS_TOKEN_COOKIE_DOMAIN": None,
    "ACCESS_TOKEN_COOKIE_SECURE": True if not DEBUG else False,
    "ACCESS_TOKEN_COOKIE_HTTP_ONLY": True,
    "ACCESS_TOKEN_COOKIE_SAMESITE": "Strict",
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=1),
    "REFRESH_TOKEN_COOKIE_NAME": "refresh_token",
    "REFRESH_TOKEN_COOKIE_PATH": "/token/refresh",
    "REFRESH_TOKEN_COOKIE_DOMAIN": None,
    "REFRESH_TOKEN_COOKIE_SECURE": True if not DEBUG else False,
    "REFRESH_TOKEN_COOKIE_HTTP_ONLY": True,
    "REFRESH_TOKEN_COOKIE_SAMESITE": "Strict",
}

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)

SPECTACULAR_SETTINGS = {
    "TITLE": "Focave",
    "DESCRIPTION": "Your personal focus cave",
    "VERSION": "1.0.0",
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "filter": True,
        # "tryItOutEnabled": True,
        "requestSnippetsEnabled": True,
    },
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    "SERVE_AUTHENTICATION": [],
    "TOS": "https://www.google.com/policies/terms/",
    "CONTACT": {"email": "focave@focave.com"},
    "LICENCE": {"name": "The GNU General Public License v3.0"},
    # "SECURITY_DEFINITIONS": {
    #     "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    # },
    # "USE_SESSION_AUTH": False,
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.hooks.postprocess_schema_enums",
        "apps.jwt.hooks.add_response_header_cookies",
    ],
}

CSRF_TRUSTED_ORIGINS = [
    "https://127.0.0.1:3000" if not DEBUG else "http://127.0.0.1:3000"
]
CSRF_FAILURE_VIEW = "apps.jwt.exceptions.csrf_failure"

CSRF_COOKIE_AGE = 31449600
CSRF_COOKIE_DOMAIN = None
CSRF_COOKIE_HTTPONLY = False  # False since we will grab it via universal-cookies
CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_PATH = "/"
CSRF_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_SECURE = False

SESSION_COOKIE_SAMESITE = "Strict"
SESSION_COOKIE_HTTPONLY = True

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
