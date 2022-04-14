from django.db import models

from movimentacao.models.base import BaseModel


class TipoEvento(BaseModel):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.descricao
