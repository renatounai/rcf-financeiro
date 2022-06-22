from django.db import models

from movimentacao.messages import TIPO_EVENTO_DESCRICAO_OBRIGATORIO, TIPO_EVENTO_DESCRICAO_REPETIDA
from movimentacao.models.base import BaseModel
from movimentacao.services.base import validate_description


class TipoEvento(BaseModel):
    descricao = models.CharField(max_length=100, unique=True)

    def before_save(self):
        validate_description(self, TIPO_EVENTO_DESCRICAO_OBRIGATORIO, TIPO_EVENTO_DESCRICAO_REPETIDA)

    def __str__(self):
        return self.descricao
