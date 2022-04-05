import datetime

from movimentacao.endpoints.base import api


class MovimentacaoError(Exception):
    pass


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

