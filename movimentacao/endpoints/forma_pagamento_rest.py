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


@api.get("/formas_de_pagamento/{forma_pagamento_id}", response=FormaPagamentoOut)
def find_by_id(request, forma_pagamento_id: int):
    return get_object_or_404(FormaPagamento, id=forma_pagamento_id)


@api.get("/formas_de_pagamento", response={200: List[FormaPagamentoOut], 204: None})
def find_all(request):
    return get_list_or_204(FormaPagamento.objects.all())


@api.post("/formas_de_pagamento", response={201: FormaPagamentoOut})
def create_employee(request, payload: FormaPagamentoIn):
    forma_pagamento = FormaPagamento()
    dict_to_model(payload.dict(), forma_pagamento)
    forma_pagamento_service.save(forma_pagamento)
    return forma_pagamento


@api.put("/formas_de_pagamento/{forma_pagamento_id}", response={200: FormaPagamentoOut})
def update_employee(request, forma_pagamento_id: int, payload: FormaPagamentoIn):
    forma_pagamento = get_object_or_404(FormaPagamento, id=forma_pagamento_id)
    dict_to_model(payload.dict(), forma_pagamento)
    forma_pagamento_service.save(forma_pagamento)
    return forma_pagamento


@api.delete("/formas_de_pagamento/{forma_pagamento_id}", response={200: None})
def delete_employee(request, forma_pagamento_id: int):
    forma_pagamento_service.delete(forma_pagamento_id)
