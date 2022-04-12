from django.http import JsonResponse
from rest_framework import status


def server_error(request, *args, **kwargs):
    """
    Generic 500 error handler.
    """
    data = {"detail": "Server Error (500)"}
    return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def bad_request(request, exception, *args, **kwargs):
    """
    Generic 400 error handler.
    """
    data = {"detail": "Bad Request (400)"}
    return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


def csrf_failure(request, reason="", *args, **kwargs):
    """
    csrf failure handler.
    """
    data = {"detail": f"CSRF Failed: {reason}"}
    return JsonResponse(data, status=status.HTTP_403_FORBIDDEN)
