# from __future__ import annotations
#
# from datetime import datetime
# from http import HTTPStatus
# from typing import TYPE_CHECKING
#
# from django.shortcuts import get_object_or_404
from ninja import Router, Schema
# from pydantic import EmailStr
#
# from utils.api_utils import get_list_or_204
# if TYPE_CHECKING:
#     from ..models.evento import Evento
#     from ..models.motivo_cancelamento import MotivoCancelamento
#     from ..models.pessoa import Pessoa
#     from ..models.status_evento import StatusEvento
#     from ..models.tipo_evento import TipoEvento
# from ..services import evento_service
#
#
# class EventoOut(Schema):
#     id: int
#     agendado_para: datetime
#     valor_cobrado: float
#     quitado: bool
#     status: int
#     motivo_cancelamento: MotivoCancelamento
#     cliente: Pessoa
#     tipo_evento: TipoEvento
#     url_galeria: str
#
#
# class PessoaOut(Schema):
#     id: int
#     nome: str
#     email: EmailStr = None
#     fone: str = None
#     instagram_user: str = None
#     facebook_user: str = None
#
#
# class EventoIn(Schema):
#     agendado_para: datetime = None
#     valor_cobrado: float = None
#     quitado: bool
#     status: StatusEvento
#     motivo_cancelamento_id: int = None
#     motivo_cancelamento_descricao: str = None
#     cliente_id: id = None
#     cliente_nome: str = None
#     tipo_evento_id: id = None
#     tipo_evento_descricao: str = None
#     url_galeria: str = None
#     gratuito: bool
#
#
router = Router()
#
#
# @router.get("/eventos/{evento_id}", response=EventoOut)
# def find_by_id(_, evento_id: int):
#     return EventoOut(get_object_or_404(Evento, id=evento_id))
#
#
# @router.get("/", response={HTTPStatus.NO_CONTENT: None})
# def find_all(_):
#     return get_list_or_204(Pessoa.objects.all())
#
#
# @router.post("/eventos", response={HTTPStatus.CREATED: EventoOut})
# def create_evento(_, payload: EventoIn):
#     evento = Evento()
#     evento_service.save_evento_in(payload)
#     return evento
#
#
# @router.put("/eventos/{evento_id}", response={HTTPStatus.OK: EventoOut})
# def update_evento(_, evento_id: int, payload: EventoIn):
#     evento = get_object_or_404(Evento, id=evento_id)
#     evento_service.save_evento_in(payload)
#     return evento
#
#
# @router.delete("/eventos/{evento_id}", response={HTTPStatus.OK: None})
# def delete_evento(_, evento_id: int):
#     get_object_or_404(Evento, id=evento_id).delete()
