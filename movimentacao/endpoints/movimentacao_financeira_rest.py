import datetime

from ninja import Schema, Router

from .rest import create_crud
from ..models.movimentacao_financeira import MovimentacaoFinanceira
from ..models.tipo_lancamento import TipoLancamento


class MovimentacaoFinanceiraOut(Schema):
    id: int
    evento_id: int
    forma_pagamento_id: int
    valor: float
    data_lancamento: datetime.datetime
    tipo_lancamento: TipoLancamento


class MovimentacaoFinanceiraIn(Schema):
    evento_id: int
    forma_pagamento_id: int
    valor: float
    tipo_lancamento: TipoLancamento
    data_lancamento: datetime.datetime = None


router = Router()
create_crud(router, MovimentacaoFinanceira, MovimentacaoFinanceiraIn, MovimentacaoFinanceiraOut)
