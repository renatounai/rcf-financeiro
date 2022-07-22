from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.shortcuts import get_object_or_404
from ninja.errors import ValidationError

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
        if self.gratuito:
            self.valor_cobrado = 0

    @staticmethod
    def from_event_in(event_in, event_id: int = None):
        if event_id:
            event = Event.objects.get(pk=event_id)
        else:
            event = Event()

        event.agendado_para = event_in.agendado_para
        event.valor_cobrado = event_in.valor_cobrado
        event.quitado = event_in.quitado
        event.status = event_in.status
        event.url_galeria = event_in.url_galeria
        event.gratuito = event_in.gratuito

        if event_in.event_type_id:
            event.event_type = get_object_or_404(EventType, id=event_in.event_type_id)
        if event_in.cliente_id:
            event.cliente = get_object_or_404(Person, id=event_in.cliente_id)
        if event_in.cancelation_reason_id:
            event.cancelation_reason = get_object_or_404(CancelationReason, id=event_in.cancelation_reason_id)

        return event

    @classmethod
    def save_event_in(cls, event_in, event_id: int = None):
        event = Event.from_event_in(event_in, event_id)

        if event_in.event_type_id is None and is_not_empty(event_in.event_type_descricao):
            event_type = EventType(descricao=event_in.event_type_descricao)
            event_type.save()
            event.event_type = event_type

        if event_in.cliente_id is None and is_not_empty(event_in.cliente_nome):
            person = Person(nome=event_in.cliente_nome)
            person.save()
            event.cliente = person

        event._set_cancelation_reason(event_in)

        if not event.is_cancelado and event.cancelation_reason_id:
            raise ValidationError(EVENTO_MOTIVO_CANCELAMENTO_FORA_DO_STATUS_CANCELED)

        event.save()
        return event

    def cancelar(self, cancelation_reason_in):
        self.status = EventStatus.CANCELED

        if cancelation_reason_in.cancelation_reason_id:
            self.cancelation_reason = get_object_or_404(
                CancelationReason, id=cancelation_reason_in.cancelation_reason_id)
        self._set_cancelation_reason(cancelation_reason_in)

        self.save()
        return self

    @classmethod
    def get(cls, pk: int):
        try:
            return cls.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise FinancialTransactionError(EVENTO_NOT_FOUND)

    def _set_cancelation_reason(self, event_in):
        if event_in.cancelation_reason_id is None and is_not_empty(event_in.cancelation_reason_descricao):
            cancelation_reason = CancelationReason(descricao=event_in.cancelation_reason_descricao)
            cancelation_reason.save()
            self.cancelation_reason = cancelation_reason

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
