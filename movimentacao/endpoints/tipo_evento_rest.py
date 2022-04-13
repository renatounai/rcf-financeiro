from http import HTTPStatus
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Schema, Router

from utils.api_utils import get_list_or_204
from ..models.tipo_evento import TipoEvento
from ..services import tipo_evento_service


class TipoEventoOut(Schema):
    id: int
    descricao: str


class TipoEventoIn(Schema):
    descricao: str


router = Router()


@router.get("/{tipo_evento_id}", response=TipoEventoOut)
def find_by_id(_, tipo_evento_id: int):
    return get_object_or_404(TipoEvento, id=tipo_evento_id)


@router.get("/", response={HTTPStatus.OK: List[TipoEventoOut], HTTPStatus.NO_CONTENT: None})
def find_all(_):
    return get_list_or_204(TipoEvento.objects.all())


@router.post("/", response={HTTPStatus.CREATED: TipoEventoOut})
def create_tipo_evento(_, payload: TipoEventoIn):
    tipo_evento = TipoEvento(descricao=payload.descricao)
    tipo_evento_service.save(tipo_evento)
    return tipo_evento


@router.put("/{tipo_evento_id}", response={HTTPStatus.OK: TipoEventoOut})
def update_tipo_evento(_, tipo_evento_id: int, payload: TipoEventoIn):
    tipo_evento = get_object_or_404(TipoEvento, id=tipo_evento_id)
    tipo_evento.descricao = payload.descricao
    tipo_evento_service.save(tipo_evento)
    return tipo_evento


@router.delete("/{tipo_evento_id}", response={HTTPStatus.OK: None})
def delete_tipo_evento(_, tipo_evento_id: int):
    get_object_or_404(TipoEvento, id=tipo_evento_id).delete()
