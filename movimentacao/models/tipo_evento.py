from django.db import models

from movimentacao.messages import TIPO_EVENTO_DESCRICAO_OBRIGATORIO, TIPO_EVENTO_DESCRICAO_REPETIDA
from movimentacao.models.base import BaseModel


class TipoEvento(BaseModel):
    descricao = models.CharField(max_length=100, unique=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self._validate_description(TIPO_EVENTO_DESCRICAO_OBRIGATORIO, TIPO_EVENTO_DESCRICAO_REPETIDA)
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.descricao
