from ninja import Schema, Router

from .rest import create_crud
from ..models.payment_method import PaymentMethod


class PaymentMethodOut(Schema):
    id: int
    descricao: str


class PaymentMethodIn(Schema):
    descricao: str


router = Router()
create_crud(router, PaymentMethod, PaymentMethodIn, PaymentMethodOut)
