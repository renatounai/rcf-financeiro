from django.db import models

from movimentacao.messages import TIPO_EVENTO_DESCRICAO_OBRIGATORIO, TIPO_EVENTO_DESCRICAO_REPETIDA
from movimentacao.models.base import BaseModel


class TipoEvento(BaseModel):
    descricao = models.CharField(max_length=100, unique=True)

    def clean(self):
        self._validate_description(TIPO_EVENTO_DESCRICAO_OBRIGATORIO, TIPO_EVENTO_DESCRICAO_REPETIDA)

    def __str__(self):
        return self.descricao
