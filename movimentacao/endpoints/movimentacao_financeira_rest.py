import datetime
from http import HTTPStatus
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Schema, Router

from utils.api_utils import get_list_or_204, dict_to_model
from ..models.movimentacao_financeira import MovimentacaoFinanceira
from ..models.tipo_lancamento import TipoLancamento
from ..services import movimentacao_financeira_service


class MovimentacaoFinanceiraOut(Schema):
    id: int
    evento_id: int
    forma_pagamento_id: int
    valor: float
    data_lancamento: datetime.datetime
    tipo_lancamento: TipoLancamento


class MovimentacaoFinanceiraIn(Schema):
    evento_id: int
    forma_pagamento_id: int
    valor: float
    tipo_lancamento: TipoLancamento


router = Router()


@router.get("/{movimentacao_financeira_id}", response=MovimentacaoFinanceiraOut)
def find_by_id(_, movimentacao_financeira_id: int):
    return get_object_or_404(MovimentacaoFinanceira, id=movimentacao_financeira_id)


@router.get("/", response={HTTPStatus.OK: List[MovimentacaoFinanceiraOut], HTTPStatus.NO_CONTENT: None})
def find_all(_):
    return get_list_or_204(MovimentacaoFinanceira.objects.all())


@router.post("/", response={HTTPStatus.CREATED: MovimentacaoFinanceiraOut})
def create_movimentacao_financeira(_, payload: MovimentacaoFinanceiraIn):
    movimentacao_financeira = MovimentacaoFinanceira()
    dict_to_model(payload.dict(), movimentacao_financeira)
    movimentacao_financeira_service.save(movimentacao_financeira)
    return movimentacao_financeira


@router.put("/{movimentacao_financeira_id}", response={HTTPStatus.OK: MovimentacaoFinanceiraOut})
def update_movimentacao_financeira(_, movimentacao_financeira_id: int, payload: MovimentacaoFinanceiraIn):
    movimentacao_financeira = get_object_or_404(MovimentacaoFinanceira, id=movimentacao_financeira_id)
    dict_to_model(payload.dict(), movimentacao_financeira)
    movimentacao_financeira_service.save(movimentacao_financeira)
    return movimentacao_financeira


@router.delete("/{movimentacao_financeira_id}", response={HTTPStatus.OK: None})
def delete_movimentacao_financeira(_, movimentacao_financeira_id: int):
    get_object_or_404(MovimentacaoFinanceira, id=movimentacao_financeira_id).delete()
