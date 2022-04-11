from django.db import models


class TipoLancamento(models.TextChoices):
    CREDITO = 'C', "Crédito"
    DEBITO = 'D', "Débito"
