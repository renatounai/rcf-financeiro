from http import HTTPStatus

from django.contrib.auth import authenticate
from ninja import Router
from ninja import Schema
from ninja.errors import HttpError
from rest_framework_simplejwt.tokens import RefreshToken


class AuthSchema(Schema):
    username: str
    password: str


class JWTPairSchema(Schema):
    refresh: str
    access: str


router = Router()


@router.post('/login', response={HTTPStatus.OK: JWTPairSchema}, auth=None)
def login(_, auth: AuthSchema):
    user = authenticate(**auth.dict())
    if user:
        refresh = RefreshToken.for_user(user)
        return JWTPairSchema(refresh=str(refresh), access=str(refresh.access_token))

    raise HttpError(401, "Not authorized")
