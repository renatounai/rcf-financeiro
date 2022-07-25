from ninja import Router

from .rest import create_crud
from .schemas import PaymentMethodIn, PaymentMethodOut
from ..models.payment_method import PaymentMethod


router = Router()
create_crud(router, PaymentMethod, PaymentMethodIn, PaymentMethodOut)
