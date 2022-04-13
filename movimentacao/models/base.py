from django.db import models
from django.db.models import Manager

from utils.string_utils import is_empty


class ObjectWithDescription:
    objects: Manager

    def __init__(self, descricao: str, pk: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.descricao = descricao
        self.id = pk


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _validate_description(self: ObjectWithDescription, msg_obrigatorio, msg_repeated):
        from movimentacao.exceptions.handler import MovimentacaoError

        if is_empty(self.descricao):
            raise MovimentacaoError(msg_obrigatorio)

        if not self.id:
            exists = self.__class__.objects.filter(descricao__iexact=self.descricao).exists()
            if exists:
                raise MovimentacaoError(msg_repeated)

    class Meta:
        abstract = True
