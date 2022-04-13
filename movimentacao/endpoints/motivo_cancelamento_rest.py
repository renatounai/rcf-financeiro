from http import HTTPStatus
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Schema

from .base import api, get_list_or_204, dict_to_model
from ..models.motivo_cancelamento import MotivoCancelamento
from ..services import motivo_cancelamento_service


class MotivoCancelamentoOut(Schema):
    id: int
    descricao: str


class MotivoCancelamentoIn(Schema):
    descricao: str


@api.get("/motivos_cancelamento/{motivo_cancelamento_id}", response=MotivoCancelamentoOut)
def find_by_id(_, motivo_cancelamento_id: int):
    return get_object_or_404(MotivoCancelamento, id=motivo_cancelamento_id)


@api.get("/motivos_cancelamento", response={HTTPStatus.OK: List[MotivoCancelamentoOut], HTTPStatus.NO_CONTENT: None})
def find_all(_):
    return get_list_or_204(MotivoCancelamento.objects.all())


@api.post("/motivos_cancelamento", response={HTTPStatus.CREATED: MotivoCancelamentoOut})
def create_evento(_, payload: MotivoCancelamentoIn):
    motivo_cancelamento = MotivoCancelamento()
    dict_to_model(payload.dict(), motivo_cancelamento)
    motivo_cancelamento_service.save(motivo_cancelamento)
    return motivo_cancelamento


@api.put("/motivos_cancelamento/{motivo_cancelamento_id}", response={HTTPStatus.OK: MotivoCancelamentoOut})
def update_evento(_, motivo_cancelamento_id: int, payload: MotivoCancelamentoIn):
    motivo_cancelamento = get_object_or_404(MotivoCancelamento, id=motivo_cancelamento_id)
    dict_to_model(payload.dict(), motivo_cancelamento)
    motivo_cancelamento_service.save(motivo_cancelamento)
    return motivo_cancelamento


@api.delete("/motivos_cancelamento/{motivo_cancelamento_id}", response={HTTPStatus.OK: None})
def delete_evento(_, motivo_cancelamento_id: int):
    get_object_or_404(MotivoCancelamento, id=motivo_cancelamento_id).delete()
