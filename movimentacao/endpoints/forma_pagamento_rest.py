from http import HTTPStatus
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Schema

from .base import api, get_list_or_204, dict_to_model
from ..models.forma_pagamento import FormaPagamento
from ..services import forma_pagamento_service


class FormaPagamentoOut(Schema):
    id: int
    descricao: str


class FormaPagamentoIn(Schema):
    descricao: str


@api.get("/formas_pagamento/{forma_pagamento_id}", response=FormaPagamentoOut)
def find_by_id(_, forma_pagamento_id: int):
    return get_object_or_404(FormaPagamento, id=forma_pagamento_id)


@api.get("/formas_pagamento", response={HTTPStatus.OK: List[FormaPagamentoOut], HTTPStatus.NO_CONTENT: None})
def find_all(_):
    return get_list_or_204(FormaPagamento.objects.all())


@api.post("/formas_pagamento", response={HTTPStatus.CREATED: FormaPagamentoOut})
def create_forma_pagamento(_, payload: FormaPagamentoIn):
    forma_pagamento = FormaPagamento()
    dict_to_model(payload.dict(), forma_pagamento)
    forma_pagamento_service.save(forma_pagamento)
    return forma_pagamento


@api.put("/formas_pagamento/{forma_pagamento_id}", response={HTTPStatus.OK: FormaPagamentoOut})
def update_forma_pagamento(_, forma_pagamento_id: int, payload: FormaPagamentoIn):
    forma_pagamento = get_object_or_404(FormaPagamento, id=forma_pagamento_id)
    dict_to_model(payload.dict(), forma_pagamento)
    forma_pagamento_service.save(forma_pagamento)
    return forma_pagamento


@api.delete("/formas_pagamento/{forma_pagamento_id}", response={HTTPStatus.OK: None})
def delete_forma_pagamento(_, forma_pagamento_id: int):
    get_object_or_404(FormaPagamento, id=forma_pagamento_id).delete()
