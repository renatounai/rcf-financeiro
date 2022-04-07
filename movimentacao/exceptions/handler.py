import datetime

from movimentacao.endpoints.base import api
from movimentacao.exceptions.movimentacao_error import MovimentacaoError


@api.exception_handler(MovimentacaoError)
def validation_error(request, exc):
    return api.create_response(
        request,
        {
            "message": str(exc),
            "timestamp": datetime.datetime.now()
        },
        status=400,
    )
