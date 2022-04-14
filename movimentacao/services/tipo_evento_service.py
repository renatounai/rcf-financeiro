from movimentacao.messages import TIPO_EVENTO_DESCRICAO_OBRIGATORIO, TIPO_EVENTO_DESCRICAO_REPETIDA
from movimentacao.models.tipo_evento import TipoEvento
from movimentacao.services.base import validate_description


def save(tipo_evento: TipoEvento):
    validate_description(tipo_evento, TIPO_EVENTO_DESCRICAO_OBRIGATORIO, TIPO_EVENTO_DESCRICAO_REPETIDA)

    tipo_evento.full_clean()
    tipo_evento.save()
