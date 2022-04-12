from movimentacao.models.tipo_evento import TipoEvento


def save(tipo_evento: TipoEvento):
    tipo_evento.full_clean()
    tipo_evento.save()
