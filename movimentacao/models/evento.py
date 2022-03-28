from datetime import datetime

from django.db import models

from movimentacao.models.base import BaseModel
from movimentacao.models.motivo_cancelamento import MotivoCancelamento
from movimentacao.models.pessoa import Pessoa
from movimentacao.models.status_evento import STATUS_EVENTO, NEGOCIANDO, AGENDADO
from movimentacao.models.tipo_evento import TipoEvento


class Evento(BaseModel):
    agendado_para = models.DateTimeField(null=True)
    valor_cobrado = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    quitado = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS_EVENTO, default=NEGOCIANDO)
    motivo_cancelamento = models.ForeignKey(MotivoCancelamento, on_delete=models.PROTECT, null=True)
    cliente = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.PROTECT)
    url_galeria = models.URLField()

    def agendar_para(self, horario_realizacao: datetime):
        if horario_realizacao is None:
            raise ValueError("O horário de realização do evento é obrigatório!")

        if self.status != NEGOCIANDO:
            raise ValueError("Só é possível agendar eventos que ainda estão em negociação")

        self.agendado_para = horario_realizacao
        self.status = AGENDADO

    def __str__(self):
        return f'{self.tipo_evento.descricao} {self.cliente.nome} {self.agendado_para}'
