import datetime

from ninja import Schema, Router

from .rest import create_crud
from ..models.financial_transaction import FinancialTransaction
from ..models.financial_transaction_type import FinancialTransactionType


class FinancialTransactionOut(Schema):
    id: int
    event_id: int
    payment_method_id: int
    valor: float
    data_lancamento: datetime.datetime
    financial_transaction_type: FinancialTransactionType


class FinancialTransactionIn(Schema):
    event_id: int
    payment_method_id: int
    valor: float
    financial_transaction_type: FinancialTransactionType
    data_lancamento: datetime.datetime = None


router = Router()
create_crud(router, FinancialTransaction, FinancialTransactionIn, FinancialTransactionOut)
