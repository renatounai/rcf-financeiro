from ninja import Schema, Router

from .rest import create_crud
from ..models.tipo_evento import TipoEvento


class TipoEventoOut(Schema):
    id: int
    descricao: str


class TipoEventoIn(Schema):
    descricao: str


router = Router()
create_crud(router, TipoEvento, TipoEventoIn, TipoEventoOut)
