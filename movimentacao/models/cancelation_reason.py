from django.db import models

from movimentacao.messages import MOTIVO_CANCELAMENTO_DESCRICAO_OBRIGATORIO, MOTIVO_CANCELAMENTO_DESCRICAO_REPETIDA
from movimentacao.models.base import BaseModel
from movimentacao.services.base import validate_description


class CancelationReason(BaseModel):
    descricao = models.CharField(max_length=200, unique=True)

    def before_save(self):
        validate_description(
            self,
            MOTIVO_CANCELAMENTO_DESCRICAO_OBRIGATORIO,
            MOTIVO_CANCELAMENTO_DESCRICAO_REPETIDA
        )

    def __str__(self):
        return self.descricao
