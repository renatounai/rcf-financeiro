from django.db import models
from django.utils import timezone

from movimentacao.exceptions.MovimentacaoError import MovimentacaoError
from movimentacao.messages import MOVIMENTACAO_FINANCEIRA_EVENTO_OBRIGATORIO, \
    MOVIMENTACAO_FINANCEIRA_FORMA_PAGAMENTO_OBRIGATORIO, MOVIMENTACAO_FINANCEIRA_VALOR_OBRIGATORIO, \
    MOVIMENTACAO_FINANCEIRA_VALOR_NEGATIVO, MOVIMENTACAO_FINANCEIRA_TIPO_LANCAMENTO_OBRIGATORIO
from movimentacao.models.base import BaseModel
from movimentacao.models.evento import Evento
from movimentacao.models.forma_pagamento import FormaPagamento
from movimentacao.models.tipo_lancamento import TipoLancamento


class MovimentacaoFinanceira(BaseModel):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=9, decimal_places=2)
    data_lancamento = models.DateTimeField()
    tipo_lancamento = models.CharField(max_length=1, choices=TipoLancamento.choices)

    def before_save(self):
        if not self.evento_id:
            raise MovimentacaoError(MOVIMENTACAO_FINANCEIRA_EVENTO_OBRIGATORIO)

        if not self.forma_pagamento_id:
            raise MovimentacaoError(MOVIMENTACAO_FINANCEIRA_FORMA_PAGAMENTO_OBRIGATORIO)

        if not self.valor:
            raise MovimentacaoError(MOVIMENTACAO_FINANCEIRA_VALOR_OBRIGATORIO)

        if self.valor < 0:
            raise MovimentacaoError(MOVIMENTACAO_FINANCEIRA_VALOR_NEGATIVO)

        if not self.tipo_lancamento:
            raise MovimentacaoError(MOVIMENTACAO_FINANCEIRA_TIPO_LANCAMENTO_OBRIGATORIO)

        if not self.data_lancamento:
            self.data_lancamento = timezone.now()

    def __str__(self):
        return f'{self.evento.tipo_evento.descricao} ' \
               f'{self.evento.cliente}, ' \
               f'{self.tipo_lancamento} ' \
               f'{self.valor} no ' \
               f'{self.forma_pagamento} em ' \
               f'{self.data_lancamento}'
