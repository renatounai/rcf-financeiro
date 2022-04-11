from django.db import models

from movimentacao.exceptions.movimentacao_error import MovimentacaoError
from movimentacao.messages import PESSOA_NOME_OBRIGATORIO
from movimentacao.models.base import BaseModel


class Pessoa(BaseModel):
    nome = models.CharField(max_length=200, blank=False)
    email = models.EmailField(null=True)
    fone = models.CharField(null=True, max_length=20)
    instagram_user = models.CharField(max_length=100, null=True)
    facebook_user = models.CharField(max_length=100, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.nome or not self.nome.strip():
            raise MovimentacaoError(PESSOA_NOME_OBRIGATORIO)

        # remove both the domais and the query string
        if self.instagram_user:
            user = self.instagram_user.split("/")
            user = user[-1].split("?")
            self.instagram_user = user[0]

        if self.facebook_user:
            user = self.facebook_user.split("/")
            user = user[-1].split("?")
            self.facebook_user = user[0]

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.nome
