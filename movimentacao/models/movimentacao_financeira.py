from django.db import models

from movimentacao.models.base import BaseModel
from movimentacao.models.forma_pagamento import FormaPagamento
from movimentacao.models.evento import Evento
from movimentacao.models.tipo_lancamento import TipoLancamento


class MovimentacaoFinanceira(BaseModel):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=9, decimal_places=2)
    data_lancamento = models.DateTimeField()
    tipo_lancamento = models.CharField(max_length=1, choices=TipoLancamento.choices, default=TipoLancamento.CREDITO)

    def __str__(self):
        return f'{self.evento.tipo_evento.descricao} ' \
               f'{self.evento.cliente}, ' \
               f'{self.tipo_lancamento} ' \
               f'{self.valor} no ' \
               f'{self.forma_pagamento} em ' \
               f'{self.data_lancamento}'
