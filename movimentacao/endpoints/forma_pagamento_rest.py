from typing import List

from django.shortcuts import get_object_or_404
from ninja import Schema

from .base import api, get_list_or_204, dict_to_model, HTTP_STATUS_OK, HTTP_STATUS_NO_CONTENT, HTTP_STATUS_CREATED
from ..models.forma_pagamento import FormaPagamento
from ..services import forma_pagamento_service


class FormaPagamentoOut(Schema):
    id: int
    descricao: str


class FormaPagamentoIn(Schema):
    descricao: str


@api.get("/formas_de_pagamento/{forma_pagamento_id}", response=FormaPagamentoOut)
def find_by_id(_, forma_pagamento_id: int):
    return get_object_or_404(FormaPagamento, id=forma_pagamento_id)


@api.get("/formas_de_pagamento", response={HTTP_STATUS_OK: List[FormaPagamentoOut], HTTP_STATUS_NO_CONTENT: None})
def find_all(_):
    return get_list_or_204(FormaPagamento.objects.all())


@api.post("/formas_de_pagamento", response={HTTP_STATUS_CREATED: FormaPagamentoOut})
def create_forma_pagamento(_, payload: FormaPagamentoIn):
    forma_pagamento = FormaPagamento()
    dict_to_model(payload.dict(), forma_pagamento)
    forma_pagamento.save()
    return forma_pagamento


@api.put("/formas_de_pagamento/{forma_pagamento_id}", response={HTTP_STATUS_OK: FormaPagamentoOut})
def update_forma_pagamento(_, forma_pagamento_id: int, payload: FormaPagamentoIn):
    forma_pagamento = get_object_or_404(FormaPagamento, id=forma_pagamento_id)
    dict_to_model(payload.dict(), forma_pagamento)
    forma_pagamento.save()
    return forma_pagamento


@api.delete("/formas_de_pagamento/{forma_pagamento_id}", response={HTTP_STATUS_OK: None})
def delete_forma_pagamento(_, forma_pagamento_id: int):
    forma_pagamento_service.delete(forma_pagamento_id)
