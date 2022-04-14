from django.db.models import Manager
from ninja.errors import ValidationError

from movimentacao.exceptions.MovimentacaoError import MovimentacaoError
from utils.string_utils import is_empty


class ObjectWithDescription:
    objects: Manager

    def __init__(self, descricao: str, pk: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.descricao = descricao
        self.id = pk


def validate_description(object_with_description: ObjectWithDescription, msg_obrigatorio, msg_repeated):
    if is_empty(object_with_description.descricao):
        raise ValidationError(msg_obrigatorio)

    if not object_with_description.id:
        manager = object_with_description.__class__.objects
        exists = manager.filter(descricao__iexact=object_with_description.descricao).exists()
        if exists:
            raise ValidationError(msg_repeated)
