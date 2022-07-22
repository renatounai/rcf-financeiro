from ninja import Schema, Router

from .rest import create_crud
from ..models.event_type import EventType


class EventTypeOut(Schema):
    id: int
    descricao: str


class EventTypeIn(Schema):
    descricao: str


router = Router()
create_crud(router, EventType, EventTypeIn, EventTypeOut)
