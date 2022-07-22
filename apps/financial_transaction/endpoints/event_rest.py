from datetime import datetime
from http import HTTPStatus
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router, Schema

from ..models.event import Event
from ..models.event_status import EventStatus


class ClienteOut(Schema):
    id: int
    nome: str


class EventOut(Schema):
    id: int
    agendado_para: datetime = None
    valor_cobrado: float = None
    quitado: bool
    status: EventStatus
    url_galeria: str = None
    cliente: ClienteOut
    event_type_id: int


class EventIn(Schema):
    valor_cobrado: float = None
    quitado: bool
    status: EventStatus
    gratuito: bool
    cliente_id: int = None
    cliente_nome: str = None
    event_type_id: int = None
    event_type_descricao: str = None
    cancelation_reason_id: int = None
    cancelation_reason_descricao: str = None
    agendado_para: datetime = None
    url_galeria: str = None


class CancelamentoIn(Schema):
    cancelation_reason_id: int = None
    cancelation_reason_descricao: str = None


router = Router()


@router.get("/{event_id}", response=EventOut)
def find_by_id(_, event_id: int):
    return get_object_or_404(Event, id=event_id)


@router.get("/", response={HTTPStatus.OK: List[EventOut], HTTPStatus.NO_CONTENT: None})
def find_all(_):
    return Event.objects.all()


@router.post("/", response={HTTPStatus.CREATED: EventOut})
def create_event(_, payload: EventIn):
    return Event.save_event_in(payload)


@router.put("/{event_id}", response={HTTPStatus.OK: EventOut})
def update_event(_, event_id: int, payload: EventIn):
    event = Event.save_event_in(payload, event_id)
    return event


@router.put("/cancelar/{event_id}", response={HTTPStatus.OK: EventOut})
def cancelar_event(_, event_id: int, cancelamento_in: CancelamentoIn):
    event = Event.get(event_id)
    return event.cancelar(cancelamento_in)


@router.delete("/{event_id}", response={HTTPStatus.OK: None})
def delete_event(_, event_id: int):
    get_object_or_404(Event, id=event_id).delete()
