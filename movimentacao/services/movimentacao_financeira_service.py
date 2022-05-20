from datetime import timezone

from django.utils import timezone

from movimentacao.exceptions.MovimentacaoError import MovimentacaoError
from movimentacao.messages import MOVIMENTACAO_FINANCEIRA_EVENTO_OBRIGATORIO, \
    MOVIMENTACAO_FINANCEIRA_FORMA_PAGAMENTO_OBRIGATORIO, MOVIMENTACAO_FINANCEIRA_VALOR_OBRIGATORIO, \
    MOVIMENTACAO_FINANCEIRA_VALOR_NEGATIVO, MOVIMENTACAO_FINANCEIRA_TIPO_LANCAMENTO_OBRIGATORIO
from movimentacao.models.movimentacao_financeira import MovimentacaoFinanceira


def save(movimentacao_financeira: MovimentacaoFinanceira):
    if not movimentacao_financeira.evento_id:
        raise MovimentacaoError(MOVIMENTACAO_FINANCEIRA_EVENTO_OBRIGATORIO)

    if not movimentacao_financeira.forma_pagamento_id:
        raise MovimentacaoError(MOVIMENTACAO_FINANCEIRA_FORMA_PAGAMENTO_OBRIGATORIO)

    if not movimentacao_financeira.valor:
        raise MovimentacaoError(MOVIMENTACAO_FINANCEIRA_VALOR_OBRIGATORIO)

    if movimentacao_financeira.valor < 0:
        raise MovimentacaoError(MOVIMENTACAO_FINANCEIRA_VALOR_NEGATIVO)

    if not movimentacao_financeira.tipo_lancamento:
        raise MovimentacaoError(MOVIMENTACAO_FINANCEIRA_TIPO_LANCAMENTO_OBRIGATORIO)

    if not movimentacao_financeira.data_lancamento:
        movimentacao_financeira.data_lancamento = timezone.now()

    movimentacao_financeira.full_clean()
    movimentacao_financeira.save()
