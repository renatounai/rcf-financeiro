from ninja import NinjaAPI

from movimentacao.endpoints.forma_pagamento_rest import router as formas_pagamento_router
from movimentacao.endpoints.motivo_cancelamento_rest import router as motivos_cancelamento_router
from movimentacao.endpoints.pessoa_rest import router as pessoas_router
from movimentacao.endpoints.tipo_evento_rest import router as tipos_evento_router
from movimentacao.endpoints.evento_rest import router as eventos_router


api = NinjaAPI()
api.add_router("/formas_pagamento", formas_pagamento_router)
api.add_router("/motivos_cancelamento", motivos_cancelamento_router)
api.add_router("/pessoas", pessoas_router)
api.add_router("/tipos_evento", tipos_evento_router)
api.add_router("/eventos", eventos_router)


