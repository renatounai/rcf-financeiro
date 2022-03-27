from datetime import datetime
from time import timezone
from typing import List, Any, Type

from django.shortcuts import get_object_or_404, get_list_or_404
from ninja import Schema

from .base import api, get_list_or_204
from ..models import FormaPagamento
from ..services import forma_pagamento_service


class FormaPagamentoOut(Schema):
    id: int
    descricao: str
    updated_at: datetime


class FormaPagamentoIn(Schema):
    descricao: str


@api.get("/formas_de_pagamento/{forma_pagamento_id}", response=FormaPagamentoOut)
def find_by_id(request, forma_pagamento_id: int):
    return get_object_or_404(FormaPagamento, id=forma_pagamento_id)


@api.get("/formas_de_pagamento", response={200: List[FormaPagamentoOut], 204: None})
def find_all(request):
    return get_list_or_204(FormaPagamento.objects.all())


@api.post("/formas_de_pagamento")
def create_employee(request, payload: FormaPagamentoIn):
    forma_pagamento = FormaPagamento(descricao=payload.descricao)
    forma_pagamento_service.save(forma_pagamento)
    return {"id": forma_pagamento.id}


@api.put("/formas_de_pagamento/{forma_pagamento_id}")
def update_employee(request, forma_pagamento_id: int, payload: FormaPagamentoIn):
    forma_pagamento = get_object_or_404(FormaPagamento, id=forma_pagamento_id)
    forma_pagamento.descricao = payload.descricao
    forma_pagamento_service.save(forma_pagamento)
    return {"success": True}


@api.delete("/formas_de_pagamento/{forma_pagamento_id}")
def delete_employee(request, forma_pagamento_id: int):
    forma_pagamento = get_object_or_404(FormaPagamento, id=forma_pagamento_id)
    forma_pagamento.delete()
    return {"success": True}
