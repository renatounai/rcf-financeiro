import datetime

from django.core.exceptions import ValidationError as DjangoValidationError
from ninja.errors import ValidationError

from movimentacao.endpoints.api import api


class MovimentacaoError(Exception):
    pass


def _error_400(request, exc):
    return api.create_response(
        request,
        {
            "message": str(exc),
            "timestamp": datetime.datetime.now()
        },
        status=400,
    )


@api.exception_handler(MovimentacaoError)
def movimentacao_error(request, exc):
    return _error_400(request, exc)


@api.exception_handler(ValidationError)
def validation_error(request, exc):
    return _error_400(request, exc)


@api.exception_handler(DjangoValidationError)
def django_validation_error(request, exc):
    return _error_400(request, exc)
