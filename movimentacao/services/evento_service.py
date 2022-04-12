from movimentacao.models.evento import Evento


def save(evento: Evento):
    evento.full_clean()
    evento.save()