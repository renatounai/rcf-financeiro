from ninja import Schema, Router
from pydantic import EmailStr

from .rest import create_crud
from ..models.pessoa import Pessoa


class PessoaOut(Schema):
    id: int
    nome: str
    email: EmailStr = None
    fone: str = None
    instagram_user: str = None
    facebook_user: str = None


class PessoaIn(Schema):
    nome: str
    email: EmailStr = None
    fone: str = None
    instagram_user: str = None
    facebook_user: str = None


router = Router()
create_crud(router, Pessoa, PessoaIn, PessoaOut)
