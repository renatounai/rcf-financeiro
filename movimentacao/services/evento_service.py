from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from movimentacao.exceptions.movimentacao_error import MovimentacaoError
from movimentacao.messages import EVENTO_STATUS_OBRIGATORIO, EVENTO_TIPO_EVENTO_OBRIGATORIO, \
    EVENTO_CLIENTE_OBRIGATORIO, \
    EVENTO_OBRIGATORIO
from movimentacao.models.evento import Evento


def _validate(evento: Evento) -> None:
    if not evento:
        raise MovimentacaoError(EVENTO_OBRIGATORIO)

    if not evento.cliente:
        raise MovimentacaoError(EVENTO_CLIENTE_OBRIGATORIO)

    if not evento.tipo_evento:
        raise MovimentacaoError(EVENTO_TIPO_EVENTO_OBRIGATORIO)

    if not evento.status:
        raise MovimentacaoError(EVENTO_STATUS_OBRIGATORIO)


def save(evento: Evento) -> None:
    evento.objects.save()


def delete(evento_id: int) -> None:
    evento = get_object_or_404(Evento, id=evento_id)
    evento.delete()


@receiver(pre_save, sender=Evento)
def _before_save(instance: Evento, **_) -> None:
    _validate(instance)
