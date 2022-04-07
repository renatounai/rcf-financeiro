from django.db import models


class ObjectWithDescription(models.Model):

    def __init__(self, descricao: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.descricao = descricao
