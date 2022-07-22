from django.db import models

from apps.financial_transaction.messages import TIPO_EVENTO_DESCRICAO_OBRIGATORIO, TIPO_EVENTO_DESCRICAO_REPETIDA
from apps.financial_transaction.models.base import BaseModel
from apps.financial_transaction.services.base import validate_description


class EventType(BaseModel):
    descricao = models.CharField(max_length=100, unique=True)

    def before_save(self):
        validate_description(self, TIPO_EVENTO_DESCRICAO_OBRIGATORIO, TIPO_EVENTO_DESCRICAO_REPETIDA)

    def __str__(self):
        return self.descricao
