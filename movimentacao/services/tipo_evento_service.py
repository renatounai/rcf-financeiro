from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from movimentacao.exceptions.movimentacao_error import MovimentacaoError
from movimentacao.messages import TIPO_EVENTO_DESCRICAO_REPETIDA, TIPO_EVENTO_DESCRICAO_OBRIGATORIO
from movimentacao.models.tipo_evento import TipoEvento


def _validate(tipo_evento: TipoEvento) -> None:
    if not tipo_evento.descricao or not tipo_evento.descricao.strip():
        raise MovimentacaoError(TIPO_EVENTO_DESCRICAO_OBRIGATORIO)

    if not tipo_evento.id:
        exists = TipoEvento.objects.filter(descricao__iexact=tipo_evento.descricao).exists()
        if exists:
            raise MovimentacaoError(TIPO_EVENTO_DESCRICAO_REPETIDA)


def save(tipo_evento: TipoEvento) -> None:
    tipo_evento.save()


def delete(tipo_evento_id: int):
    tipo_evento = get_object_or_404(TipoEvento, id=tipo_evento_id)
    tipo_evento.delete()


@receiver(pre_save, sender=TipoEvento)
def _before_save(instance: TipoEvento, **_) -> None:
    _validate(instance)
