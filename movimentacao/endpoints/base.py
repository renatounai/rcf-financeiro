from django.db.models import QuerySet
from ninja import NinjaAPI


api = NinjaAPI()


def get_list_or_204(queryset: QuerySet):
    obj_list = list(queryset)
    if not obj_list:
        return 204, obj_list
    return obj_list
