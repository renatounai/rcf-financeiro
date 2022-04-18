from datetime import datetime

from django.db import models
from django.shortcuts import get_object_or_404

from movimentacao.models.base import BaseModel
from movimentacao.models.motivo_cancelamento import MotivoCancelamento
from movimentacao.models.pessoa import Pessoa
from movimentacao.models.status_evento import StatusEvento
from movimentacao.models.tipo_evento import TipoEvento
from utils.string_utils import is_empty


class Evento(BaseModel):
    agendado_para = models.DateTimeField(null=True, blank=True)
    valor_cobrado = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    quitado = models.BooleanField(default=False)
    status = models.IntegerField(choices=StatusEvento.choices, default=StatusEvento.NEGOCIANDO)
    motivo_cancelamento = models.ForeignKey(MotivoCancelamento, on_delete=models.PROTECT, null=True, blank=True)
    cliente = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.PROTECT)
    url_galeria = models.URLField(null=True, blank=True)
    gratuito = models.BooleanField(default=False)

    def __init__(self, evento=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not evento:
            return

        self.agendado_para = evento.agendado_para
        self.valor_cobrado = evento.valor_cobrado
        self.quitado = evento.quitado
        self.status = evento.status
        self.url_galeria = evento.url_galeria
        self.gratuito = evento.gratuito
        if evento.tipo_evento_id:
            self.tipo_evento = get_object_or_404(TipoEvento, id=evento.tipo_evento_id)
        if evento.cliente_id:
            self.cliente = get_object_or_404(Pessoa, id=evento.cliente_id)
        if evento.motivo_cancelamento_id:
            self.motivo_cancelamento = get_object_or_404(MotivoCancelamento, id=evento.motivo_cancelamento_id)

    def clean(self):
        if self.gratuito:
            self.valor_cobrado = 0

    @property
    def is_cancelado(self):
        return self.status == StatusEvento.CANCELADO

    def agendar_para(self, horario_realizacao: datetime):
        if horario_realizacao is None:
            raise ValueError("O horário de realização do evento é obrigatório!")

        if self.status != StatusEvento.NEGOCIANDO:
            raise ValueError("Só é possível agendar eventos que ainda estão em negociação")

        self.agendado_para = horario_realizacao
        self.status = StatusEvento.AGENDADO

    def __str__(self):
        return f'{self.tipo_evento.descricao} {self.cliente.nome} {self.agendado_para}'
