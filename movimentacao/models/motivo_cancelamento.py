from django.db import models

from movimentacao.models.base import BaseModel


class MotivoCancelamento(BaseModel):
    descricao = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.descricao
