from django.db.models import Manager


class ObjectWithDescription:
    objects: Manager

    def __init__(self, descricao: str, pk: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.descricao = descricao
        self.id = pk

