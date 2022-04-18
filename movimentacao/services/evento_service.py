from __future__ import annotations

from typing import TYPE_CHECKING

from ninja.errors import ValidationError

from movimentacao.messages import EVENTO_MOTIVO_CANCELAMENTO_FORA_DO_STATUS_CANCELADO
from movimentacao.models.evento import Evento
from movimentacao.models.motivo_cancelamento import MotivoCancelamento
from movimentacao.models.pessoa import Pessoa
from movimentacao.models.tipo_evento import TipoEvento

if TYPE_CHECKING:
    from movimentacao.endpoints.evento_rest import EventoIn
from movimentacao.services import tipo_evento_service, pessoa_service, motivo_cancelamento_service
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

    if evento_in.motivo_cancelamento_id is None and is_not_empty(evento_in.motivo_cancelamento_descricao):
        motivo_cancelamento = MotivoCancelamento(descricao=evento_in.motivo_cancelamento_descricao)
        motivo_cancelamento_service.save(motivo_cancelamento)
        evento.motivo_cancelamento = motivo_cancelamento

    if not evento.is_cancelado and evento.motivo_cancelamento_id:
        raise ValidationError(EVENTO_MOTIVO_CANCELAMENTO_FORA_DO_STATUS_CANCELADO)

    save(evento)
    return evento
