from typing import List

from django.shortcuts import get_object_or_404
from ninja import Schema

from .base import api, get_list_or_204, dict_to_model
from ..models.pessoa import Pessoa
from ..services import pessoa_service


class PessoaOut(Schema):
    id: int
    descricao: str
    email: str
    fone: str
    instagram_user: str
    facebook_user: str


class PessoaIn(Schema):
    descricao: str
    email: str
    fone: str
    instagram_user: str
    facebook_user: str


@api.get("/pessoas/{pessoa_id}", response=PessoaOut)
def find_by_id(_, pessoa_id: int):
    return get_object_or_404(Pessoa, id=pessoa_id)


@api.get("/pessoas", response={200: List[PessoaOut], 204: None})
def find_all(_):
    return get_list_or_204(Pessoa.objects.all())


@api.post("/pessoas", response={201: PessoaOut})
def create_employee(_, payload: PessoaIn):
    pessoa = Pessoa()
    dict_to_model(payload.dict(), pessoa)
    pessoa_service.save(pessoa)
    return pessoa


@api.put("/pessoas/{pessoa_id}", response={200: PessoaOut})
def update_employee(_, pessoa_id: int, payload: PessoaIn):
    pessoa = get_object_or_404(Pessoa, id=pessoa_id)
    dict_to_model(payload.dict(), pessoa)
    pessoa_service.save(pessoa)
    return pessoa


@api.delete("/pessoas/{pessoa_id}", response={200: None})
def delete_employee(_, pessoa_id: int):
    pessoa_service.delete(pessoa_id)
