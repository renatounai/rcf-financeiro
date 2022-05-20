from datetime import datetime
from http import HTTPStatus
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router, Schema

from ..models.evento import Evento
from ..services import evento_service


class ClienteOut(Schema):
    id: int
    nome: str


class EventoOut(Schema):
    id: int
    agendado_para: datetime = None
    valor_cobrado: float = None
    quitado: bool
    status: int
    url_galeria: str = None
    cliente: ClienteOut
    tipo_evento_id: int


class EventoIn(Schema):
    valor_cobrado: float = None
    quitado: bool
    status: int
    gratuito: bool
    cliente_id: int = None
    cliente_nome: str = None
    tipo_evento_id: int = None
    tipo_evento_descricao: str = None
    motivo_cancelamento_id: int = None
    motivo_cancelamento_descricao: str = None
    agendado_para: datetime = None
    url_galeria: str = None


class CancelamentoIn(Schema):
    motivo_cancelamento_id: int = None
    motivo_cancelamento_descricao: str = None


router = Router()


@router.get("/{evento_id}", response=EventoOut)
def find_by_id(_, evento_id: int):
    return get_object_or_404(Evento, id=evento_id)


@router.get("/", response={HTTPStatus.OK: List[EventoOut] , HTTPStatus.NO_CONTENT: None})
def find_all(_):
    return Evento.objects.all()


@router.post("/", response={HTTPStatus.CREATED: EventoOut})
def create_evento(_, payload: EventoIn):
    return evento_service.save_evento_in(payload)


@router.put("/{evento_id}", response={HTTPStatus.OK: EventoOut})
def update_evento(_, evento_id: int, payload: EventoIn):
    evento = evento_service.save_evento_in(payload, evento_id)
    return evento


@router.put("/cancelar/{evento_id}", response={HTTPStatus.OK: EventoOut})
def cancelar_evento(_, evento_id: int, motivo_cancelamento_in: CancelamentoIn):
    return evento_service.cancelar(evento_id, motivo_cancelamento_in)


@router.delete("/{evento_id}", response={HTTPStatus.OK: None})
def delete_evento(_, evento_id: int):
    get_object_or_404(Evento, id=evento_id).delete()
