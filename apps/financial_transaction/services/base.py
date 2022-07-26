from ninja.errors import ValidationError

from apps.financial_transaction.exceptions import FinancialTransactionError
from utils.string_utils import is_empty


def validate_description(object_with_description, msg_obrigatorio, msg_repeated):
    if is_empty(object_with_description.description):
        raise ValidationError(msg_obrigatorio)

    manager = object_with_description.__class__.objects
    exists = manager.filter(description__iexact=object_with_description.description)\
        .exclude(id=object_with_description.id)\
        .exists()
    if exists:
        raise FinancialTransactionError.FinancialTransactionError(msg_repeated)
