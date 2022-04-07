from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from movimentacao.exceptions.movimentacao_error import MovimentacaoError
from movimentacao.messages import PESSOA_NOME_OBRIGATORIO
from movimentacao.models.base import BaseModel


class Pessoa(BaseModel):
    nome = models.CharField(max_length=200, blank=False)
    email = models.EmailField()
    fone = PhoneNumberField()
    instagram_user = models.CharField(max_length=100)
    facebook_user = models.CharField(max_length=100)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.nome or not self.nome.strip():
            raise MovimentacaoError(PESSOA_NOME_OBRIGATORIO)

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.nome
