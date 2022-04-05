from django.shortcuts import get_object_or_404

from movimentacao.exceptions.movimentacao_error import MovimentacaoError
from movimentacao.models.motivo_cancelamento import MotivoCancelamento


def _validate(motivo_cancelamento: MotivoCancelamento) -> None:
    if not motivo_cancelamento:
        raise MovimentacaoError("O motivo de cancelamento é obrigatório!")

    if not motivo_cancelamento.descricao or not motivo_cancelamento.descricao.strip():
        raise MovimentacaoError("A descrição do motivo de cancelamento é obrigatória!")


def save(motivo_cancelamento: MotivoCancelamento) -> None:
    _validate(motivo_cancelamento)
    motivo_cancelamento.save()


def delete(motivo_cancelamento_id: int):
    motivo_cancelamento = get_object_or_404(MotivoCancelamento, id=motivo_cancelamento_id)
    motivo_cancelamento.delete()
