from django.db.models import QuerySet
from ninja import NinjaAPI

from movimentacao.models.base import BaseModel

HTTP_STATUS_OK = 200
HTTP_STATUS_CREATED = 201
HTTP_STATUS_NO_CONTENT = 204
HTTP_STATUS_BAD_REQUEST = 400
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_UNPROCESSABLE_ENTITY = 422

api = NinjaAPI()


def get_list_or_204(queryset: QuerySet):
    obj_list = list(queryset)
    if not obj_list:
        return 204, obj_list
    return obj_list


def dict_to_model(dictionary: dict, model: BaseModel):
    for attr, value in dictionary.items():
        setattr(model, attr, value)
