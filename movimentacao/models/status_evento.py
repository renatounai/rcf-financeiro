from django.db import models


class StatusEvento(models.IntegerChoices):
    NEGOCIANDO = 1, "Negociando"
    AGENDADO = 2, "Agendado"
    REALIZADO = 3, "Realizado"
    EM_ESCOLHA = 4, "Em escolha"
    EM_TRATAMENTO = 5, "Em tratamento"
    ENTREGUE = 6, "Entregue"
    CANCELADO = 7, "Cancelado"
