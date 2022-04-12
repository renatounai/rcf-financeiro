from django.db import models

from movimentacao.messages import MOTIVO_CANCELAMENTO_DESCRICAO_OBRIGATORIO, MOTIVO_CANCELAMENTO_DESCRICAO_REPETIDA
from movimentacao.models.base import BaseModel


class MotivoCancelamento(BaseModel):
    descricao = models.CharField(max_length=200, unique=True)

    def clean(self):
        self._validate_description(MOTIVO_CANCELAMENTO_DESCRICAO_OBRIGATORIO, MOTIVO_CANCELAMENTO_DESCRICAO_REPETIDA)

    def __str__(self):
        return self.descricao
