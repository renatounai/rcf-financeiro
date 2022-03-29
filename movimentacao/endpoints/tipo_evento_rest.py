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


@api.get("/tipos_de_evento/{tipo_evento_id}", response=TipoEventoOut)
def find_by_id(request, tipo_evento_id: int):
    return get_object_or_404(TipoEvento, id=tipo_evento_id)


@api.get("/tipos_de_evento", response={200: List[TipoEventoOut], 204: None})
def find_all(request):
    return get_list_or_204(TipoEvento.objects.all())


@api.post("/tipos_de_evento", response={201: TipoEventoOut})
def create_employee(request, payload: TipoEventoIn):
    tipo_evento = TipoEvento(descricao=payload.descricao)
    tipo_evento_service.save(tipo_evento)
    return tipo_evento


@api.put("/tipos_de_evento/{tipo_evento_id}", response={200: TipoEventoOut})
def update_employee(request, tipo_evento_id: int, payload: TipoEventoIn):
    tipo_evento = get_object_or_404(TipoEvento, id=tipo_evento_id)
    tipo_evento.descricao = payload.descricao
    tipo_evento_service.save(tipo_evento)
    return tipo_evento


@api.delete("/tipos_de_evento/{tipo_evento_id}", response={200: None})
def delete_employee(request, tipo_evento_id: int):
    tipo_evento_service.delete(tipo_evento_id)
