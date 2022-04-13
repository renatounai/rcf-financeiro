from http import HTTPStatus
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Schema

from .base import api, get_list_or_204
from ..models.tipo_evento import TipoEvento
from ..services import tipo_evento_service


class TipoEventoOut(Schema):
    id: int
    descricao: str


class TipoEventoIn(Schema):
    descricao: str


@api.get("/tipos_evento/{tipo_evento_id}", response=TipoEventoOut)
def find_by_id(_, tipo_evento_id: int):
    return get_object_or_404(TipoEvento, id=tipo_evento_id)


@api.get("/tipos_evento", response={HTTPStatus.OK: List[TipoEventoOut], HTTPStatus.NO_CONTENT: None})
def find_all(_):
    return get_list_or_204(TipoEvento.objects.all())


@api.post("/tipos_evento", response={HTTPStatus.CREATED: TipoEventoOut})
def create_evento(_, payload: TipoEventoIn):
    tipo_evento = TipoEvento(descricao=payload.descricao)
    tipo_evento_service.save(tipo_evento)
    return tipo_evento


@api.put("/tipos_evento/{tipo_evento_id}", response={HTTPStatus.OK: TipoEventoOut})
def update_evento(_, tipo_evento_id: int, payload: TipoEventoIn):
    tipo_evento = get_object_or_404(TipoEvento, id=tipo_evento_id)
    tipo_evento.descricao = payload.descricao
    tipo_evento_service.save(tipo_evento)
    return tipo_evento


@api.delete("/tipos_evento/{tipo_evento_id}", response={HTTPStatus.OK: None})
def delete_evento(_, tipo_evento_id: int):
    get_object_or_404(TipoEvento, id=tipo_evento_id).delete()
