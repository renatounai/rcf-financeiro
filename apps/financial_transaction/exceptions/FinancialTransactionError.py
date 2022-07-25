from django.core.exceptions import ValidationError


class FinancialTransactionError(ValidationError):
    pass
