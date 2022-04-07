from django.db import models

from movimentacao.exceptions.movimentacao_error import MovimentacaoError
from movimentacao.models.ObjectWithDescription import ObjectWithDescription


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _validate_description(self: ObjectWithDescription, msg_obrigatorio, msg_repeated):
        if not hasattr(self, 'descricao'):
            return

        if not self.descricao or not self.descricao.strip():
            raise MovimentacaoError(msg_obrigatorio)

        if not self.id:
            exists = self.__class__.objects.filter(descricao__iexact=self.descricao).exists()
            if exists:
                raise MovimentacaoError(msg_repeated)

    class Meta:
        abstract = True
