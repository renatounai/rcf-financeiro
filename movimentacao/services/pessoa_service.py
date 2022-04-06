from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from movimentacao.exceptions.movimentacao_error import MovimentacaoError
from movimentacao.messages import PESSOA_NOME_OBRIGATORIO
from movimentacao.models.pessoa import Pessoa


def _validate(pessoa: Pessoa) -> None:
    if not pessoa.nome or not pessoa.nome.strip():
        raise MovimentacaoError(PESSOA_NOME_OBRIGATORIO)


def save(pessoa: Pessoa) -> None:
    pessoa.save()


def delete(pessoa_id: int):
    pessoa = get_object_or_404(Pessoa, id=pessoa_id)
    pessoa.delete()


@receiver(pre_save, sender=Pessoa)
def _before_save(instance: Pessoa, **_) -> None:
    _validate(instance)
