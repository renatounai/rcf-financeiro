from movimentacao.models.pessoa import Pessoa


def save(pessoa: Pessoa):
    pessoa.full_clean()
    pessoa.save()
