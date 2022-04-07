from django.db import models

from movimentacao.messages import MOTIVO_CANCELAMENTO_DESCRICAO_OBRIGATORIO, MOTIVO_CANCELAMENTO_DESCRICAO_REPETIDA
from movimentacao.models.base import BaseModel


class MotivoCancelamento(BaseModel):
    descricao = models.CharField(max_length=200, unique=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self._validate_description(MOTIVO_CANCELAMENTO_DESCRICAO_OBRIGATORIO, MOTIVO_CANCELAMENTO_DESCRICAO_REPETIDA)
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.descricao
