from ninja import NinjaAPI

api = NinjaAPI()


def get_list_or_204(list_of_models):
    obj_list = list(list_of_models)
    if not obj_list:
        return 204, obj_list
    return obj_list


def dict_to_model(dictionary: dict, model):
    for attr, value in dictionary.items():
        setattr(model, attr, value)
