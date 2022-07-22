from ninja import Schema, Router
from pydantic import EmailStr

from .rest import create_crud
from ..models.person import Person


class PersonOut(Schema):
    id: int
    nome: str
    email: EmailStr = None
    fone: str = None
    instagram_user: str = None
    facebook_user: str = None


class PersonIn(Schema):
    nome: str
    email: EmailStr = None
    fone: str = None
    instagram_user: str = None
    facebook_user: str = None


router = Router()
create_crud(router, Person, PersonIn, PersonOut)
