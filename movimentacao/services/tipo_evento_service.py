from django.shortcuts import get_object_or_404

from movimentacao.exceptions.movimentacao_error import MovimentacaoError
from movimentacao.models.tipo_evento import TipoEvento


def _validate(tipo_evento: TipoEvento) -> None:
    if not tipo_evento:
        raise MovimentacaoError("O Tipo de Evento é obrigatório!")

    if not tipo_evento.descricao or not tipo_evento.descricao.strip():
        raise MovimentacaoError("A descrição do tipo de evento é obrigatória!")


def save(tipo_evento: TipoEvento) -> None:
    _validate(tipo_evento)
    tipo_evento.save()


def delete(tipo_evento_id: int):
    tipo_evento = get_object_or_404(TipoEvento, id=tipo_evento_id)
    tipo_evento.delete()
