from django.db.models import QuerySet
from ninja import NinjaAPI

from movimentacao.models.base import BaseModel

api = NinjaAPI()


def get_list_or_204(queryset: QuerySet):
    obj_list = list(queryset)
    if not obj_list:
        return 204, obj_list
    return obj_list


def dict_to_model(dictionary: dict, model: BaseModel):
    for attr, value in dictionary.items():
        setattr(model, attr, value)
