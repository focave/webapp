from focave import settings
from rest_framework import serializers
from rest_framework_simplejwt import serializers as jwt_serializers


class TokenRefreshSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            settings.SIMPLE_JWT["REFRESH_TOKEN_COOKIE_NAME"]
        ] = serializers.CharField(write_only=True)
        self.fields[
            settings.SIMPLE_JWT["ACCESS_TOKEN_COOKIE_NAME"]
        ] = serializers.CharField(read_only=True)

    def validate(self, attrs):
        data = jwt_serializers.TokenRefreshSerializer().validate(
            attrs={"refresh": attrs[settings.SIMPLE_JWT["REFRESH_TOKEN_COOKIE_NAME"]]}
        )
        return {settings.SIMPLE_JWT["ACCESS_TOKEN_COOKIE_NAME"]: data["access"]}


class TokenVerifySerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            settings.SIMPLE_JWT["ACCESS_TOKEN_COOKIE_NAME"]
        ] = serializers.CharField(write_only=True)

    def validate(self, attrs):
        data = jwt_serializers.TokenVerifySerializer().validate(
            attrs={"token": attrs[settings.SIMPLE_JWT["ACCESS_TOKEN_COOKIE_NAME"]]}
        )
        return data
