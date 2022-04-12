import datetime

from focave import settings


def get_access_token_example():
    result = ""

    result += f"{settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE_NAME']}=<token>; "
    result += f"expires={settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']}; "
    if settings.SIMPLE_JWT["ACCESS_TOKEN_COOKIE_HTTP_ONLY"]:
        result += "HttpOnly; "
    result += f"Path={settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE_PATH']}; "
    result += f"SameSite={settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE_SAMESITE']}; "
    if settings.SIMPLE_JWT["ACCESS_TOKEN_COOKIE_SECURE"]:
        result += "Secure; "

    return result


def get_deleted_access_token_example():
    result = ""

    result += f"{settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE_NAME']}=\"\"; "
    result += f"expires={datetime.datetime(1970, 1, 1, hour=0, minute=0, second=0)}; "
    result += "Max-age=0; "
    result += f"Path={settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE_PATH']}; "

    return result


def get_refresh_token_example():
    result = ""

    result += f"{settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_NAME']}=<token>; "
    result += f"expires={settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']}; "
    if settings.SIMPLE_JWT["REFRESH_TOKEN_COOKIE_HTTP_ONLY"]:
        result += "HttpOnly; "
    result += f"Path={settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_PATH']}; "
    result += f"SameSite={settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_SAMESITE']}; "
    if settings.SIMPLE_JWT["REFRESH_TOKEN_COOKIE_SECURE"]:
        result += "Secure; "

    return result


def get_deleted_refresh_token_example():
    result = ""

    result += f"{settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_NAME']}=\"\"; "
    result += f"expires={datetime.datetime(1970, 1, 1, hour=0, minute=0, second=0)}; "
    result += "Max-age=0; "
    result += f"Path={settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_PATH']}; "

    return result


def get_csrftoken_example():
    result = ""

    result += f"{settings.CSRF_COOKIE_NAME}=<token>; "
    result += f"Max-age={settings.CSRF_COOKIE_AGE}; "
    if settings.CSRF_COOKIE_HTTPONLY:
        result += "HttpOnly; "
    result += f"Path={settings.CSRF_COOKIE_PATH}; "
    result += f"SameSite={settings.CSRF_COOKIE_SAMESITE}; "
    if settings.CSRF_COOKIE_SECURE:
        result += "Secure; "

    return result


def get_deleted_csrftoken_example():
    result = ""

    result += f'{settings.CSRF_COOKIE_NAME}=""; '
    result += f"expires={datetime.datetime(1970, 1, 1, hour=0, minute=0, second=0)}; "
    result += "Max-age=0; "
    result += f"Path={settings.CSRF_COOKIE_PATH}; "

    return result


def add_response_header_cookies(result, generator, request, public):
    result["paths"]["/token/"]["post"]["responses"]["200"]["headers"] = {
        "Set-Cookie": {
            "description": settings.SIMPLE_JWT["ACCESS_TOKEN_COOKIE_NAME"],
            "schema": {"type": "string", "example": get_access_token_example()},
        },
        "Set-Cookie ": {
            "description": settings.SIMPLE_JWT["REFRESH_TOKEN_COOKIE_NAME"],
            "schema": {"type": "string", "example": get_refresh_token_example()},
        },
        "Set-Cookie  ": {
            "description": settings.CSRF_COOKIE_NAME,
            "schema": {"type": "string", "example": get_csrftoken_example()},
        },
    }

    result["paths"]["/token/refresh/"]["post"]["responses"]["200"]["headers"] = {
        "Set-Cookie": {
            "description": settings.SIMPLE_JWT["ACCESS_TOKEN_COOKIE_NAME"],
            "schema": {"type": "string", "example": get_access_token_example()},
        },
    }

    result["paths"]["/token/delete/"]["post"]["responses"]["200"]["headers"] = {
        "Set-Cookie": {
            "description": settings.SIMPLE_JWT["ACCESS_TOKEN_COOKIE_NAME"],
            "schema": {"type": "string", "example": get_deleted_access_token_example()},
        },
        "Set-Cookie ": {
            "description": settings.SIMPLE_JWT["REFRESH_TOKEN_COOKIE_NAME"],
            "schema": {
                "type": "string",
                "example": get_deleted_refresh_token_example(),
            },
        },
        "Set-Cookie  ": {
            "description": settings.CSRF_COOKIE_NAME,
            "schema": {"type": "string", "example": get_deleted_csrftoken_example()},
        },
    }
    return result
