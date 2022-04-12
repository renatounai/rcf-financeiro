from django.db import models

from movimentacao.messages import FORMA_PAGAMENTO_DESCRICAO_OBRIGATORIA, FORMA_PAGAMENTO_DESCRICAO_REPETIDA
from movimentacao.models.base import BaseModel


class FormaPagamento(BaseModel):
    descricao = models.CharField(max_length=30, blank=False, unique=True, null=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, error_messages=None):
        self._validate_description(FORMA_PAGAMENTO_DESCRICAO_OBRIGATORIA, FORMA_PAGAMENTO_DESCRICAO_REPETIDA)
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.descricao
