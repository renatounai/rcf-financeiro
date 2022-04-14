from __future__ import annotations

from typing import TYPE_CHECKING

from movimentacao.models.evento import Evento

if TYPE_CHECKING:
    from movimentacao.endpoints.evento_rest import EventoIn
    from movimentacao.models.pessoa import Pessoa
    from movimentacao.models.tipo_evento import TipoEvento
from movimentacao.services import tipo_evento_service, pessoa_service
from utils.string_utils import is_not_empty


def save(evento: Evento):
    evento.full_clean()
    evento.save()


def save_evento_in(evento_in: EventoIn):
    evento = Evento(evento_in)

    if evento_in.tipo_evento_id is None and is_not_empty(evento_in.tipo_evento_descricao):
        tipo_evento = TipoEvento(descricao=evento_in.tipo_evento_descricao)
        tipo_evento_service.save(tipo_evento)
        evento.tipo_evento = tipo_evento

    if evento_in.cliente_id is None and is_not_empty(evento_in.cliente_nome):
        pessoa = Pessoa(nome=evento_in.cliente_nome)
        pessoa_service.save(pessoa)
        evento.cliente = pessoa

    save(evento)
    return evento
