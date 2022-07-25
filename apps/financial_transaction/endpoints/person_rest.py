from ninja import Router

from .rest import create_crud
from .schemas import PersonIn, PersonOut
from ..models.person import Person


router = Router()
create_crud(router, Person, PersonIn, PersonOut)
