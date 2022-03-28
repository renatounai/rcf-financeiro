from django.db import models

from movimentacao.models.base import BaseModel


class MotivoCancelamento(BaseModel):
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return self.descricao
