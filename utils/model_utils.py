from movimentacao.models.base import BaseModel


def is_model_empty(model: BaseModel):
    return not model or not model.id
