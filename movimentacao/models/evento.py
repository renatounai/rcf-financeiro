from datetime import datetime
from typing import TYPE_CHECKING

from django.db import models

from movimentacao.exceptions.movimentacao_error import MovimentacaoError
from movimentacao.messages import EVENTO_CLIENTE_OBRIGATORIO, EVENTO_TIPO_EVENTO_OBRIGATORIO, EVENTO_STATUS_OBRIGATORIO
from movimentacao.models.base import BaseModel
from movimentacao.models.motivo_cancelamento import MotivoCancelamento
from movimentacao.models.pessoa import Pessoa
from movimentacao.models.status_evento import StatusEvento
from movimentacao.models.tipo_evento import TipoEvento


class Evento(BaseModel):
    agendado_para = models.DateTimeField(null=True)
    valor_cobrado = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    quitado = models.BooleanField(default=False)
    status = models.IntegerField(choices=StatusEvento.choices, default=StatusEvento.NEGOCIANDO)
    motivo_cancelamento = models.ForeignKey(MotivoCancelamento, on_delete=models.PROTECT, null=True)
    cliente = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.PROTECT)
    url_galeria = models.URLField()
    gratuito = models.BooleanField(default=False)

    def __init__(self, evento = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not evento:
            return

        self.agendado_para = evento.agendado_para
        self.valor_cobrado = evento.valor_cobrado
        self.quitado = evento.quitado
        self.status = evento.status
        self.url_galeria = evento.url_galeria
        self.gratuito = evento.gratuito

    def clean(self):
        if not self.cliente:
            raise MovimentacaoError(EVENTO_CLIENTE_OBRIGATORIO)

        if not self.tipo_evento:
            raise MovimentacaoError(EVENTO_TIPO_EVENTO_OBRIGATORIO)

        if not self.status:
            raise MovimentacaoError(EVENTO_STATUS_OBRIGATORIO)

        if self.gratuito:
            self.valor_cobrado = 0

    def agendar_para(self, horario_realizacao: datetime):
        if horario_realizacao is None:
            raise ValueError("O horário de realização do evento é obrigatório!")

        if self.status != StatusEvento.NEGOCIANDO:
            raise ValueError("Só é possível agendar eventos que ainda estão em negociação")

        self.agendado_para = horario_realizacao
        self.status = StatusEvento.AGENDADO

    def __str__(self):
        return f'{self.tipo_evento.descricao} {self.cliente.nome} {self.agendado_para}'
