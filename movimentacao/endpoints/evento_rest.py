from datetime import datetime
from decimal import Decimal
from http import HTTPStatus
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Schema

from .base import api, get_list_or_204, dict_to_model
from ..models.evento import Evento
from ..services import evento_service


class EventoOut(Schema):
    id: int
    agendado_para: datetime
    valor_cobrado: float
    quitado: bool
    status: int
    motivo_cancelamento: str
    motivo_cancelamento_id: str
    cliente: str
    cliente_id: str
    tipo_evento: str
    url_galeria: str

    def __init__(self, evento: Evento, **kwargs):
        super().__init__(**kwargs)
        self.id = evento.id
        self.agendado_para = evento.agendado_para
        self.valor_cobrado: Decimal = evento.valor_cobrado
        self.quitado = evento.quitado
        self.status = evento.status
        self.motivo_cancelamento = evento.motivo_cancelamento.descricao
        self.motivo_cancelamento_id: int = evento.motivo_cancelamento.id
        self.cliente = evento.cliente.nome
        self.cliente.id = evento.cliente.id
        self.tipo_evento = evento.tipo_evento.descricao
        self.tipo_evento_id = evento.tipo_evento.id
        self.url_galeria = evento.url_galeria


class EventoIn(Schema):
    agendado_para: datetime
    valor_cobrado: float
    quitado: bool
    status: int
    motivo_cancelamento_id: int
    motivo_cancelamento: str
    cliente_id: id
    cliente: str
    tipo_evento_id: id
    tipo_evento: str
    url_galeria: str


@api.get("/eventos/{evento_id}", response=EventoOut)
def find_by_id(_, evento_id: int):
    return EventoOut(get_object_or_404(Evento, id=evento_id))


@api.get("/eventos", response={HTTPStatus.OK: List[EventoOut], HTTPStatus.NO_CONTENT: None})
def find_all(_):
    eventos = map(EventoOut, Evento.objects.all())
    return get_list_or_204(eventos)


@api.post("/eventos", response={HTTPStatus.CREATED: EventoOut})
def create_evento(_, payload: EventoIn):
    evento = Evento()
    dict_to_model(payload.dict(), evento)
    evento_service.save(evento)
    return evento


@api.put("/eventos/{evento_id}", response={HTTPStatus.OK: EventoOut})
def update_evento(_, evento_id: int, payload: EventoIn):
    evento = get_object_or_404(Evento, id=evento_id)
    dict_to_model(payload.dict(), evento)
    evento_service.save(evento)
    return evento


@api.delete("/eventos/{evento_id}", response={HTTPStatus.OK: None})
def delete_evento(_, evento_id: int):
    get_object_or_404(Evento, id=evento_id).delete()
