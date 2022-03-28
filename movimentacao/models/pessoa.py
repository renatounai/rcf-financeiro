from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from movimentacao.models.base import BaseModel


class Pessoa(BaseModel):
    nome = models.CharField(max_length=200, blank=False)
    email = models.EmailField()
    fone = PhoneNumberField()
    instagram_user = models.CharField(max_length=100)
    facebook_user = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
