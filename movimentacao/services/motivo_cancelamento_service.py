from movimentacao.messages import MOTIVO_CANCELAMENTO_DESCRICAO_REPETIDA, MOTIVO_CANCELAMENTO_DESCRICAO_OBRIGATORIO
from movimentacao.models.motivo_cancelamento import MotivoCancelamento
from movimentacao.services.base import validate_description


def save(motivo_cancelamento: MotivoCancelamento):
    validate_description(motivo_cancelamento, MOTIVO_CANCELAMENTO_DESCRICAO_OBRIGATORIO, MOTIVO_CANCELAMENTO_DESCRICAO_REPETIDA)
    motivo_cancelamento.full_clean()
    motivo_cancelamento.save()
