from django.db import models
from django.utils import timezone

from apps.financial_transaction.exceptions.FinancialTransactionError import FinancialTransactionError
from apps.financial_transaction.messages import MOVIMENTACAO_FINANCEIRA_EVENTO_OBRIGATORIO, \
    MOVIMENTACAO_FINANCEIRA_FORMA_PAGAMENTO_OBRIGATORIO, MOVIMENTACAO_FINANCEIRA_VALOR_OBRIGATORIO, \
    MOVIMENTACAO_FINANCEIRA_VALOR_NEGATIVO, MOVIMENTACAO_FINANCEIRA_TIPO_LANCAMENTO_OBRIGATORIO
from apps.financial_transaction.models.base import BaseModel
from apps.financial_transaction.models.event import Event
from apps.financial_transaction.models.financial_transaction_type import FinancialTransactionType
from apps.financial_transaction.models.payment_method import PaymentMethod


class FinancialTransaction(BaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=9, decimal_places=2)
    data_lancamento = models.DateTimeField()
    financial_transaction_type = models.CharField(max_length=6, choices=FinancialTransactionType.choices)

    def before_save(self):
        if not self.event_id:
            raise FinancialTransactionError(MOVIMENTACAO_FINANCEIRA_EVENTO_OBRIGATORIO)

        if not self.payment_method_id:
            raise FinancialTransactionError(MOVIMENTACAO_FINANCEIRA_FORMA_PAGAMENTO_OBRIGATORIO)

        if not self.valor:
            raise FinancialTransactionError(MOVIMENTACAO_FINANCEIRA_VALOR_OBRIGATORIO)

        if self.valor < 0:
            raise FinancialTransactionError(MOVIMENTACAO_FINANCEIRA_VALOR_NEGATIVO)

        if not self.financial_transaction_type:
            raise FinancialTransactionError(MOVIMENTACAO_FINANCEIRA_TIPO_LANCAMENTO_OBRIGATORIO)

        if not self.data_lancamento:
            self.data_lancamento = timezone.now()

    def __str__(self):
        return f'{self.event.event_type.descricao} ' \
               f'{self.event.cliente}, ' \
               f'{self.financial_transaction_type} ' \
               f'{self.valor} no ' \
               f'{self.payment_method} em ' \
               f'{self.data_lancamento}'
