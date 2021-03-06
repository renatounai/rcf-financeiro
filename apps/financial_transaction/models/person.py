from django.db import models
from ninja.errors import ValidationError

from apps.financial_transaction.messages import PESSOA_NOME_OBRIGATORIO
from apps.financial_transaction.models.base import BaseModel
from utils.string_utils import is_empty


class Person(BaseModel):
    name = models.CharField(max_length=200, blank=False)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(null=True, max_length=20, blank=True)
    instagram_user = models.CharField(max_length=100, null=True, blank=True)
    facebook_user = models.CharField(max_length=100, null=True, blank=True)

    def before_save(self):
        if is_empty(self.name):
            raise ValidationError(PESSOA_NOME_OBRIGATORIO)

        # remove both the domain and the query string
        if self.instagram_user:
            user = self.instagram_user.split("/")
            user = user[-1].split("?")
            self.instagram_user = user[0]

        if self.facebook_user:
            user = self.facebook_user.split("/")
            user = user[-1].split("?")
            self.facebook_user = user[0]

    def __str__(self):
        return self.name
