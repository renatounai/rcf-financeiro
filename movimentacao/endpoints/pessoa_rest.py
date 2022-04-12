from http import HTTPStatus
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Schema
from pydantic import EmailStr

from .base import api, get_list_or_204, dict_to_model
from ..models.pessoa import Pessoa
from ..services import pessoa_service


class PessoaOut(Schema):
    id: int
    nome: str
    email: EmailStr = None
    fone: str = None
    instagram_user: str = None
    facebook_user: str = None


class PessoaIn(Schema):
    nome: str
    email: EmailStr = None
    fone: str = None
    instagram_user: str = None
    facebook_user: str = None


@api.get("/pessoas/{pessoa_id}", response=PessoaOut)
def find_by_id(_, pessoa_id: int):
    return get_object_or_404(Pessoa, id=pessoa_id)


@api.get("/pessoas", response={HTTPStatus.OK: List[PessoaOut], HTTPStatus.NO_CONTENT: None})
def find_all(_):
    return get_list_or_204(Pessoa.objects.all())


@api.post("/pessoas", response={HTTPStatus.CREATED: PessoaOut})
def create_evento(_, payload: PessoaIn):
    pessoa = Pessoa()
    dict_to_model(payload.dict(), pessoa)
    pessoa_service.save(pessoa)
    return pessoa


@api.put("/pessoas/{pessoa_id}", response={HTTPStatus.OK: PessoaOut})
def update_evento(_, pessoa_id: int, payload: PessoaIn):
    pessoa = get_object_or_404(Pessoa, id=pessoa_id)
    dict_to_model(payload.dict(), pessoa)
    pessoa_service.save(pessoa)
    return pessoa


@api.delete("/pessoas/{pessoa_id}", response={HTTPStatus.OK: None})
def delete_evento(_, pessoa_id: int):
    get_object_or_404(Pessoa, id=pessoa_id).delete()
