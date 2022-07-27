from typing import Optional, Any

from django.http import HttpRequest
from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from project import settings


class AuthBearer(HttpBearer):

    def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
        print(token)
        if settings.DEBUG:
            return token == "123"

        jwt_authenticator = JWTAuthentication()
        try:
            response = jwt_authenticator.authenticate(request)
            if response is not None:
                return True
            return False
        except InvalidToken:
            return False
