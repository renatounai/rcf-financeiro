from typing import List

from django.shortcuts import get_object_or_404
from ninja import Schema

from .base import api, get_list_or_204
from ..models.tipo_evento import TipoEvento


class TipoEventoOut(Schema):
    id: int
    descricao: str


class TipoEventoIn(Schema):
    descricao: str


@api.get("/tipos_evento/{tipo_evento_id}", response=TipoEventoOut)
def find_by_id(_, tipo_evento_id: int):
    return get_object_or_404(TipoEvento, id=tipo_evento_id)


@api.get("/tipos_evento", response={200: List[TipoEventoOut], 204: None})
def find_all(_):
    return get_list_or_204(TipoEvento.objects.all())


@api.post("/tipos_evento", response={201: TipoEventoOut})
def create_employee(_, payload: TipoEventoIn):
    tipo_evento = TipoEvento(descricao=payload.descricao)
    tipo_evento.save()
    return tipo_evento


@api.put("/tipos_evento/{tipo_evento_id}", response={200: TipoEventoOut})
def update_employee(_, tipo_evento_id: int, payload: TipoEventoIn):
    tipo_evento = get_object_or_404(TipoEvento, id=tipo_evento_id)
    tipo_evento.descricao = payload.descricao
    tipo_evento.save()
    return tipo_evento


@api.delete("/tipos_evento/{tipo_evento_id}", response={200: None})
def delete_employee(_, tipo_evento_id: int):
    get_object_or_404(TipoEvento, id=tipo_evento_id).delete()
