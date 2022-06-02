from datetime import datetime

from django.db import models
from django.shortcuts import get_object_or_404

from movimentacao.models.base import BaseModel
from movimentacao.models.motivo_cancelamento import MotivoCancelamento
from movimentacao.models.pessoa import Pessoa
from movimentacao.models.status_evento import StatusEvento
from movimentacao.models.tipo_evento import TipoEvento


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

    @staticmethod
    def from_evento_in(evento_in, evento_id: int = None):
        if evento_id:
            evento = Evento.objects.get(pk=evento_id)
        else:
            evento = Evento()

        evento.agendado_para = evento_in.agendado_para
        evento.valor_cobrado = evento_in.valor_cobrado
        evento.quitado = evento_in.quitado
        evento.status = evento_in.status
        evento.url_galeria = evento_in.url_galeria
        evento.gratuito = evento_in.gratuito

        if evento_in.tipo_evento_id:
            evento.tipo_evento = get_object_or_404(TipoEvento, id=evento_in.tipo_evento_id)
        if evento_in.cliente_id:
            evento.cliente = get_object_or_404(Pessoa, id=evento_in.cliente_id)
        if evento_in.motivo_cancelamento_id:
            evento.motivo_cancelamento = get_object_or_404(MotivoCancelamento, id=evento_in.motivo_cancelamento_id)

        return evento

    def clean(self):
        if self.gratuito:
            self.valor_cobrado = 0

    @property
    def is_cancelado(self) -> bool:
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
