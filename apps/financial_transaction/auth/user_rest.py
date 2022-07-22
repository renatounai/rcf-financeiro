from http import HTTPStatus

from ninja import Schema, Router

from apps.financial_transaction.auth import user_service


class User(Schema):
    email: str
    password: str


router = Router()


@router.post("/", response={HTTPStatus.CREATED: None})
def create_account(_, user: User):
    user_service.create_account(user)
