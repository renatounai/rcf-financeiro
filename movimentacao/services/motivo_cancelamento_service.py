from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from movimentacao.exceptions.movimentacao_error import MovimentacaoError
from movimentacao.messages import MOTIVO_CANCELAMENTO_DESCRICAO_OBRIGATORIO, \
    MOTIVO_CANCELAMENTO_DESCRICAO_REPETIDA
from movimentacao.models.motivo_cancelamento import MotivoCancelamento


def _validate(motivo_cancelamento: MotivoCancelamento) -> None:
    if not motivo_cancelamento.descricao or not motivo_cancelamento.descricao.strip():
        raise MovimentacaoError(MOTIVO_CANCELAMENTO_DESCRICAO_OBRIGATORIO)

    if not motivo_cancelamento.id:
        exists = MotivoCancelamento.objects.filter(descricao__iexact=motivo_cancelamento.descricao).exists()
        if exists:
            raise MovimentacaoError(MOTIVO_CANCELAMENTO_DESCRICAO_REPETIDA)


def save(motivo_cancelamento: MotivoCancelamento) -> None:
    motivo_cancelamento.save()


def delete(motivo_cancelamento_id: int):
    motivo_cancelamento = get_object_or_404(MotivoCancelamento, id=motivo_cancelamento_id)
    motivo_cancelamento.delete()


@receiver(pre_save, sender=MotivoCancelamento)
def _before_save(instance: MotivoCancelamento, **_) -> None:
    _validate(instance)
