from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from ninja.errors import ValidationError

from movimentacao.exceptions.MovimentacaoError import MovimentacaoError
from movimentacao.messages import EVENTO_MOTIVO_CANCELAMENTO_FORA_DO_STATUS_CANCELADO, EVENTO_NOT_FOUND
from movimentacao.models.evento import Evento
from movimentacao.models.motivo_cancelamento import MotivoCancelamento
from movimentacao.models.pessoa import Pessoa
from movimentacao.models.status_evento import StatusEvento
from movimentacao.models.tipo_evento import TipoEvento
from movimentacao.services import tipo_evento_service, pessoa_service, motivo_cancelamento_service
from utils.string_utils import is_not_empty


def save(evento: Evento) -> None:
    evento.full_clean()
    evento.save()


def save_evento_in(evento_in, evento_id: int = None) -> Evento:
    evento = Evento.from_evento_in(evento_in, evento_id)

    if evento_in.tipo_evento_id is None and is_not_empty(evento_in.tipo_evento_descricao):
        tipo_evento = TipoEvento(descricao=evento_in.tipo_evento_descricao)
        tipo_evento_service.save(tipo_evento)
        evento.tipo_evento = tipo_evento

    if evento_in.cliente_id is None and is_not_empty(evento_in.cliente_nome):
        pessoa = Pessoa(nome=evento_in.cliente_nome)
        pessoa_service.save(pessoa)
        evento.cliente = pessoa

    _set_motivo_cancelamento(evento, evento_in)

    if not evento.is_cancelado and evento.motivo_cancelamento_id:
        raise ValidationError(EVENTO_MOTIVO_CANCELAMENTO_FORA_DO_STATUS_CANCELADO)

    save(evento)
    return evento


def _set_motivo_cancelamento(evento: Evento, evento_in):
    if evento_in.motivo_cancelamento_id is None and is_not_empty(evento_in.motivo_cancelamento_descricao):
        motivo_cancelamento = MotivoCancelamento(descricao=evento_in.motivo_cancelamento_descricao)
        motivo_cancelamento_service.save(motivo_cancelamento)
        evento.motivo_cancelamento = motivo_cancelamento


def cancelar(evento_id, motivo_cancelamento_in) -> Evento:
    evento = Evento.objects.get(pk=evento_id)
    evento.status = StatusEvento.CANCELADO

    if motivo_cancelamento_in.motivo_cancelamento_id:
        evento.motivo_cancelamento = get_object_or_404(
            MotivoCancelamento, id=motivo_cancelamento_in.motivo_cancelamento_id)
    _set_motivo_cancelamento(evento, motivo_cancelamento_in)

    save(evento)
    return evento


def get(pk: int) -> Evento:
    try:
        return Evento.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise MovimentacaoError(EVENTO_NOT_FOUND)
