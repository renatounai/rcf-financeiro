from http import HTTPStatus
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router

from utils.api_utils import dict_to_model
from .schemas import EventOut, EventIn, CancelamentoIn
from ..models.event import Event


router = Router()


@router.get("/{event_id}", response=EventOut)
def find_by_id(_, event_id: int):
    return get_object_or_404(Event, id=event_id)


@router.get("/", response={HTTPStatus.OK: List[EventOut], HTTPStatus.NO_CONTENT: None})
def find_all(_):
    return Event.objects.all()


@router.post("/", response={HTTPStatus.CREATED: EventOut})
def create_event(_, payload: EventIn):
    event = Event(**payload.dict())
    event.save()
    return event


@router.put("/{event_id}", response={HTTPStatus.OK: EventOut})
def update_event(_, event_id: int, payload: EventIn):
    event = get_object_or_404(Event, id=event_id)
    dict_to_model(payload.dict(), event)
    event.save()
    return event


@router.put("/cancelar/{event_id}", response={HTTPStatus.NO_CONTENT: None})
def cancelar_event(_, event_id: int, cancelamento_in: CancelamentoIn):
    event = Event.get(event_id)
    event.cancelar(cancelamento_in)


@router.delete("/{event_id}", response={HTTPStatus.OK: None})
def delete_event(_, event_id: int):
    get_object_or_404(Event, id=event_id).delete()
