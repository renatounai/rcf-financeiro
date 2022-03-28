from django.db import models

from movimentacao.models.base import BaseModel


class FormaPagamento(BaseModel):
    descricao = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.descricao
