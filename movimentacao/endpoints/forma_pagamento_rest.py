from ninja import Schema, Router

from .rest import create_crud
from ..models.forma_pagamento import FormaPagamento


class FormaPagamentoOut(Schema):
    id: int
    descricao: str


class FormaPagamentoIn(Schema):
    descricao: str


router = Router()
create_crud(router, FormaPagamento, FormaPagamentoIn, FormaPagamentoOut)
