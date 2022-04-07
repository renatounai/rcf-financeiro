from django.db import models
from django.db.models import Manager

from movimentacao.exceptions.movimentacao_error import MovimentacaoError


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
        if not self.descricao or not self.descricao.strip():
            raise MovimentacaoError(msg_obrigatorio)

        if not self.id:
            exists = self.__class__.objects.filter(descricao__iexact=self.descricao).exists()
            if exists:
                raise MovimentacaoError(msg_repeated)

    class Meta:
        abstract = True
