from http import HTTPStatus

from ninja.errors import HttpError


class MovimentacaoError(HttpError):
    def __init__(self, message: str) -> None:
        super().__init__(HTTPStatus.BAD_REQUEST, message)
