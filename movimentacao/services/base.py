from django.db.models import Manager
from ninja.errors import ValidationError
from typing_extensions import Protocol

from utils.string_utils import is_empty


class ObjectWithDescription(Protocol):
    objects: Manager

    def __init__(self, descricao: str, pk: int):
        self.descricao = descricao
        self.id = pk


def validate_description(object_with_description: ObjectWithDescription, msg_obrigatorio, msg_repeated):
    if is_empty(object_with_description.descricao):
        raise ValidationError(msg_obrigatorio)

    manager = object_with_description.__class__.objects
    exists = manager.filter(descricao__iexact=object_with_description.descricao)\
        .exclude(id=object_with_description.id)\
        .exists()
    if exists:
        raise ValidationError(msg_repeated)
