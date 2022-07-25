from ninja import Router

from .rest import create_crud
from .schemas import FinancialTransactionIn, FinancialTransactionOut
from ..models.financial_transaction import FinancialTransaction


router = Router()
create_crud(router, FinancialTransaction, FinancialTransactionIn, FinancialTransactionOut)
