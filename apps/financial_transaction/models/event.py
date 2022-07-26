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
    scheduled_to = models.DateTimeField(null=True, blank=True)
    amount_charged = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    paid = models.BooleanField(default=False)
    status = models.CharField(choices=EventStatus.choices, default=EventStatus.NEGOTIATING, max_length=40)
    cancelation_reason = models.ForeignKey(CancelationReason, on_delete=models.PROTECT, null=True, blank=True)
    clients = models.ForeignKey(Person, on_delete=models.CASCADE)
    event_type = models.ForeignKey(EventType, on_delete=models.PROTECT)
    gallery_url = models.URLField(null=True, blank=True)

    def before_save(self):
        if not self.is_cancelado and self.cancelation_reason_id:
            raise ValidationError(EVENTO_MOTIVO_CANCELAMENTO_FORA_DO_STATUS_CANCELED)

    def cancelar(self, cancelation_reason_in: CancelamentoIn) -> None:
        self.status = EventStatus.CANCELED
        if cancelation_reason_in.id:
            self.cancelation_reason = get_object_or_404(CancelationReason, id=cancelation_reason_in.id)
        elif is_not_empty(cancelation_reason_in.description):
            self.cancelation_reason = CancelationReason.objects.create(description=cancelation_reason_in.description)

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

        self.scheduled_to = horario_realizacao
        self.status = EventStatus.SCHEDULED

    def __str__(self):
        return f'{self.event_type.description} {self.clients.name} {self.scheduled_to}'
