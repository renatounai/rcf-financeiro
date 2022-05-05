from ninja.errors import ValidationError

from movimentacao.models.movimentacao_financeira import MovimentacaoFinanceira
from utils.model_utils import is_model_empty

MOVIMENTACAO_FINANCEIRA_EVENTO_OBRIGATORIO = "O evento é obtigatório!"
MOVIMENTACAO_FINANCEIRA_FORMA_PAGAMENTO_OBRIGATORIO = "A forma de pagamento é obtigatória!"
MOVIMENTACAO_FINANCEIRA_VALOR_OBRIGATORIO = "O valor é obrigatório!"
MOVIMENTACAO_FINANCEIRA_VALOR_NEGATIVO = "O valor não pode ser negativo!"
MOVIMENTACAO_FINANCEIRA_TIPO_LANCAMENTO_OBRIGATORIO = "O tipo de lançamento é obrigatório!"
MOVIMENTACAO_FINANCEIRA_TIPO_LANCAMENTO_INVALIDO = "Informe um tipo de lançamento válido!"


def save(movimentacao_financeira: MovimentacaoFinanceira):
    if is_model_empty(movimentacao_financeira.evento):
        raise ValidationError(MOVIMENTACAO_FINANCEIRA_EVENTO_OBRIGATORIO)

    if is_model_empty(movimentacao_financeira.forma_pagamento):
        raise ValidationError(MOVIMENTACAO_FINANCEIRA_FORMA_PAGAMENTO_OBRIGATORIO)

    if not movimentacao_financeira.valor:
        raise ValidationError(MOVIMENTACAO_FINANCEIRA_VALOR_OBRIGATORIO)

    if movimentacao_financeira.valor < 0:
        raise ValidationError(MOVIMENTACAO_FINANCEIRA_VALOR_NEGATIVO)

    if not movimentacao_financeira.tipo_lancamento:
        raise ValidationError(MOVIMENTACAO_FINANCEIRA_TIPO_LANCAMENTO_OBRIGATORIO)

    movimentacao_financeira.full_clean()
    movimentacao_financeira.save()
