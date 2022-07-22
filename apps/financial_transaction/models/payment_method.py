from django.db import models

from apps.financial_transaction.messages import FORMA_PAGAMENTO_DESCRICAO_OBRIGATORIA, FORMA_PAGAMENTO_DESCRICAO_REPETIDA
from apps.financial_transaction.models.base import BaseModel
from apps.financial_transaction.services.base import validate_description


class PaymentMethod(BaseModel):
    descricao = models.CharField(max_length=30, blank=False, unique=True, null=False)

    def before_save(self):
        validate_description(self, FORMA_PAGAMENTO_DESCRICAO_OBRIGATORIA, FORMA_PAGAMENTO_DESCRICAO_REPETIDA)

    def __str__(self):
        return self.descricao
