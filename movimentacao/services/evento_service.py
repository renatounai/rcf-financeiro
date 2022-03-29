from django.shortcuts import get_object_or_404

from movimentacao.exceptions.movimentacao_error import MovimentacaoErro
from movimentacao.models.evento import Evento


def _validate(evento: Evento) -> None:
    if not evento:
        raise MovimentacaoErro("O evento é obrigatório!")

    if not evento.cliente:
        raise MovimentacaoErro("O cliente é obrigatório!")

    if not evento.tipo_evento:
        raise MovimentacaoErro("O tipo de evento é obrigatório!")

    if not evento.status:
        raise MovimentacaoErro("O status é obrigatório!")


def save(evento: Evento) -> None:
    _validate(evento)
    evento.save()


def delete(evento_id: int):
    evento = get_object_or_404(Evento, id=evento_id)
    evento.delete()
