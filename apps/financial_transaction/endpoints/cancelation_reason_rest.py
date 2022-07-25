from ninja import Router

from .rest import create_crud
from .schemas import CancelationReasonIn, CancelationReasonOut
from ..models.cancelation_reason import CancelationReason


router = Router()
create_crud(router, CancelationReason, CancelationReasonIn, CancelationReasonOut)
