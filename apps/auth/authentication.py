from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access = request.COOKIES.get('access')
        if access is None:
            return None
        try:
            validated_token = self.get_validated_token(access)
            return self.get_user(validated_token), validated_token
        except Exception:
            return None
