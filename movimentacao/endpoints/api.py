from django.core.exceptions import ValidationError
from ninja import NinjaAPI

from auth.auth import router as auth_router
from auth.auth_bearer import AuthBearer
from movimentacao.endpoints.evento_rest import router as eventos_router
from movimentacao.endpoints.forma_pagamento_rest import router as formas_pagamento_router
from movimentacao.endpoints.motivo_cancelamento_rest import router as motivos_cancelamento_router
from movimentacao.endpoints.movimentacao_financeira_rest import router as movimentacao_financeira_router
from movimentacao.endpoints.pessoa_rest import router as pessoas_router
from movimentacao.endpoints.tipo_evento_rest import router as tipos_evento_router

api = NinjaAPI(auth=AuthBearer())


@api.exception_handler(ValidationError)
def validation_errors(request, exc):
    return api.create_response(
        request,
        {"detail": exc.messages},
        status=400,
    )


api.add_router("/formas_pagamento", formas_pagamento_router)
api.add_router("/motivos_cancelamento", motivos_cancelamento_router)
api.add_router("/pessoas", pessoas_router)
api.add_router("/tipos_evento", tipos_evento_router)
api.add_router("/eventos", eventos_router)
api.add_router("/movimentacoes_financeiras", movimentacao_financeira_router)
api.add_router("/auth", auth_router)
