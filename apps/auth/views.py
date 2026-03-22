from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

ACCESS_COOKIE = 'access'
REFRESH_COOKIE = 'refresh'

COOKIE_SETTINGS = dict(
    httponly=True,
    secure=False,
    samesite='Lax',
    max_age=60 * 60 * 24 * 7,
)


class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            response.set_cookie(
                REFRESH_COOKIE, response.data.pop('refresh'), **COOKIE_SETTINGS
            )
            response.set_cookie(
                ACCESS_COOKIE, response.data.pop('access'), **COOKIE_SETTINGS
            )

        return response


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(REFRESH_COOKIE)
        if refresh_token:
            request._full_data = {'refresh': refresh_token}

        try:
            response = super().post(request, *args, **kwargs)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        if new_refresh := response.data.pop('refresh', None):
            response.set_cookie(REFRESH_COOKIE, new_refresh, **COOKIE_SETTINGS)

        response.set_cookie(
            ACCESS_COOKIE, response.data.pop('access'), **COOKIE_SETTINGS
        )

        return response


class CookieTokenLogoutView(APIView):
    def post(self, request):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(ACCESS_COOKIE)
        response.delete_cookie(REFRESH_COOKIE)
        return response
