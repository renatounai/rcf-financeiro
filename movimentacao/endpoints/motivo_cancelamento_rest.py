from ninja import Schema, Router

from .rest import create_crud
from ..models.motivo_cancelamento import MotivoCancelamento


class MotivoCancelamentoOut(Schema):
    id: int
    descricao: str


class MotivoCancelamentoIn(Schema):
    descricao: str


router = Router()
create_crud(router, MotivoCancelamento, MotivoCancelamentoIn, MotivoCancelamentoOut)
