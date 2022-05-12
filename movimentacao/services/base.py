from ninja.errors import ValidationError

from utils.string_utils import is_empty


def validate_description(object_with_description, msg_obrigatorio, msg_repeated):
    if is_empty(object_with_description.descricao):
        raise ValidationError(msg_obrigatorio)

    manager = object_with_description.__class__.objects
    exists = manager.filter(descricao__iexact=object_with_description.descricao)\
        .exclude(id=object_with_description.id)\
        .exists()
    if exists:
        raise ValidationError(msg_repeated)
