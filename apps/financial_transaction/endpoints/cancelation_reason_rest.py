from ninja import Schema, Router

from .rest import create_crud
from ..models.cancelation_reason import CancelationReason


class CancelationReasonOut(Schema):
    id: int
    descricao: str


class CancelationReasonIn(Schema):
    descricao: str


router = Router()
create_crud(router, CancelationReason, CancelationReasonIn, CancelationReasonOut)
