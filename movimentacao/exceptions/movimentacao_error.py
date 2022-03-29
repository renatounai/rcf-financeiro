import datetime

from movimentacao.endpoints.base import api


class MovimentacaoErro(Exception):
    pass


@api.exception_handler(MovimentacaoErro)
def validation_error(request, exc):
    return api.create_response(
        request,
        {
            "message": str(exc),
            "timestamp": datetime.datetime.now()
        },
        status=400,
    )

