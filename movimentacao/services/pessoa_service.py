from django.shortcuts import get_object_or_404

from movimentacao.exceptions.movimentacao_error import MovimentacaoError
from movimentacao.models.pessoa import Pessoa


def _validate(pessoa: Pessoa) -> None:
    if not pessoa:
        raise MovimentacaoError("A pessoa é obrigatória!")

    if not pessoa.nome or not pessoa.nome.strip():
        raise MovimentacaoError("O nome da pessoa é obrigatório!")


def save(pessoa: Pessoa) -> None:
    _validate(pessoa)
    pessoa.save()


def delete(pessoa_id: int):
    pessoa = get_object_or_404(Pessoa, id=pessoa_id)
    pessoa.delete()
