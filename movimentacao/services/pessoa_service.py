from ninja.errors import ValidationError

from movimentacao.messages import PESSOA_NOME_OBRIGATORIO
from movimentacao.models.pessoa import Pessoa
from utils.string_utils import is_empty


def save(pessoa: Pessoa):

    if is_empty(pessoa.nome):
        raise ValidationError(PESSOA_NOME_OBRIGATORIO)

    pessoa.full_clean()
    pessoa.save()
