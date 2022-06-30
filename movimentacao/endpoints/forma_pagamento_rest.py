from http import HTTPStatus
from typing import List

from django.db import models
from django.shortcuts import get_object_or_404
from ninja import Schema, Router

from utils.api_utils import dict_to_model
from ..models.forma_pagamento import FormaPagamento


class FormaPagamentoOut(Schema):
    id: int
    descricao: str


class FormaPagamentoIn(Schema):
    descricao: str


router = Router()


def create_crud(model: models.Model, schema: Schema, out_schema: Schema):
    router.get("/{pk}", response=FormaPagamentoOut)(
        lambda _, pk: get_object_or_404(model, id=pk)
    )

    router.get("/", response=List[out_schema])(
        lambda _: model.objects.all()
    )


create_crud(FormaPagamento, FormaPagamentoIn, FormaPagamentoOut)


# @router.get("/{forma_pagamento_id}", response=FormaPagamentoOut)
# def find_by_id(_, forma_pagamento_id: int):
#     return get_object_or_404(FormaPagamento, id=forma_pagamento_id)
#
#
# @router.get("/", response={HTTPStatus.OK: List[FormaPagamentoOut]})
# def find_all(_):
#     return FormaPagamento.objects.all()


@router.post("/", response={HTTPStatus.CREATED: FormaPagamentoOut})
def create_forma_pagamento(_, payload: FormaPagamentoIn):
    forma_pagamento = FormaPagamento(**payload.dict())
    forma_pagamento.save()
    return forma_pagamento


@router.put("/{forma_pagamento_id}", response={HTTPStatus.OK: FormaPagamentoOut})
def update_forma_pagamento(_, forma_pagamento_id: int, payload: FormaPagamentoIn):
    forma_pagamento = get_object_or_404(FormaPagamento, id=forma_pagamento_id)
    dict_to_model(payload.dict(), forma_pagamento)
    forma_pagamento.save()
    return forma_pagamento


@router.delete("/{forma_pagamento_id}", response={HTTPStatus.OK: None})
def delete_forma_pagamento(_, forma_pagamento_id: int):
    get_object_or_404(FormaPagamento, id=forma_pagamento_id).delete()
