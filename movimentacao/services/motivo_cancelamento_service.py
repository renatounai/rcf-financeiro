from movimentacao.models.motivo_cancelamento import MotivoCancelamento


def save(motivo_cancelamento: MotivoCancelamento):
    motivo_cancelamento.full_clean()
    motivo_cancelamento.save()
