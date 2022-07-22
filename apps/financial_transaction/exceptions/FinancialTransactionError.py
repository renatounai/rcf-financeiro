from http import HTTPStatus
from django.core.exceptions import ValidationError
from ninja.errors import HttpError


class FinancialTransactionError(ValidationError):
    pass
