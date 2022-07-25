from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.shortcuts import get_object_or_404
from ninja.errors import ValidationError

from apps.financial_transaction.endpoints.schemas import CancelamentoIn
from apps.financial_transaction.exceptions.FinancialTransactionError import FinancialTransactionError
from apps.financial_transaction.messages import EVENTO_MOTIVO_CANCELAMENTO_FORA_DO_STATUS_CANCELED, EVENTO_NOT_FOUND
from apps.financial_transaction.models.base import BaseModel
from apps.financial_transaction.models.cancelation_reason import CancelationReason
from apps.financial_transaction.models.event_status import EventStatus
from apps.financial_transaction.models.event_type import EventType
from apps.financial_transaction.models.person import Person
from utils.string_utils import is_not_empty


class Event(BaseModel):
    agendado_para = models.DateTimeField(null=True, blank=True)
    valor_cobrado = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    quitado = models.BooleanField(default=False)
    status = models.CharField(choices=EventStatus.choices, default=EventStatus.NEGOTIATING, max_length=40)
    cancelation_reason = models.ForeignKey(CancelationReason, on_delete=models.PROTECT, null=True, blank=True)
    cliente = models.ForeignKey(Person, on_delete=models.CASCADE)
    event_type = models.ForeignKey(EventType, on_delete=models.PROTECT)
    url_galeria = models.URLField(null=True, blank=True)
    gratuito = models.BooleanField(default=False)

    def before_save(self):
        if not self.is_cancelado and self.cancelation_reason_id:
            raise ValidationError(EVENTO_MOTIVO_CANCELAMENTO_FORA_DO_STATUS_CANCELED)

        if self.gratuito:
            self.valor_cobrado = 0

    def cancelar(self, cancelation_reason_in: CancelamentoIn) -> None:
        self.status = EventStatus.CANCELED
        if cancelation_reason_in.id:
            self.cancelation_reason = get_object_or_404(CancelationReason, id=cancelation_reason_in.id)
        elif is_not_empty(cancelation_reason_in.description):
            self.cancelation_reason = CancelationReason.objects.create(descricao=cancelation_reason_in.description)

        self.save()

    @classmethod
    def get(cls, pk: int):
        try:
            return cls.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise FinancialTransactionError(EVENTO_NOT_FOUND)

    @property
    def is_cancelado(self) -> bool:
        return self.status == EventStatus.CANCELED

    def agendar_para(self, horario_realizacao: datetime):
        if horario_realizacao is None:
            raise ValueError("O horário de realização do event é obrigatório!")

        if self.status != EventStatus.NEGOTIATING:
            raise ValueError("Só é possível agendar events que ainda estão em negociação")

        self.agendado_para = horario_realizacao
        self.status = EventStatus.SCHEDULED

    def __str__(self):
        return f'{self.event_type.descricao} {self.cliente.nome} {self.agendado_para}'
