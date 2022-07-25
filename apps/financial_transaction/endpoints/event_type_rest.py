from ninja import Router

from .rest import create_crud
from .schemas import EventTypeIn, EventTypeOut
from ..models.event_type import EventType

router = Router()
create_crud(router, EventType, EventTypeIn, EventTypeOut)
