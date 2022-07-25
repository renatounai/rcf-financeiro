from ninja import Schema
from pydantic import EmailStr
from pydantic.schema import datetime

from apps.financial_transaction.models.event_status import EventStatus
from apps.financial_transaction.models.financial_transaction_type import FinancialTransactionType


class EventTypeOut(Schema):
    id: int
    descricao: str


class EventTypeIn(Schema):
    descricao: str


class CancelationReasonOut(Schema):
    id: int
    descricao: str


class CancelationReasonIn(Schema):
    descricao: str


class EventType(Schema):
    id: int
    description: str = None


class CancelamentoIn(Schema):
    id: int = None
    description: str = None


class FinancialTransactionOut(Schema):
    id: int
    event_id: int
    payment_method_id: int
    valor: float
    data_lancamento: datetime
    financial_transaction_type: FinancialTransactionType


class FinancialTransactionIn(Schema):
    event_id: int
    payment_method_id: int
    valor: float
    financial_transaction_type: FinancialTransactionType
    data_lancamento: datetime = None


class PaymentMethodOut(Schema):
    id: int
    descricao: str


class PaymentMethodIn(Schema):
    descricao: str


class PersonOut(Schema):
    id: int
    nome: str
    email: EmailStr = None
    fone: str = None
    instagram_user: str = None
    facebook_user: str = None


class PersonIn(Schema):
    nome: str
    email: EmailStr = None
    fone: str = None
    instagram_user: str = None
    facebook_user: str = None


class EventIn(Schema):
    valor_cobrado: float = None
    quitado: bool
    status: EventStatus
    gratuito: bool
    cliente_id: int
    cancelation_reason_id: int = None
    event_type_id: int
    agendado_para: datetime = None
    url_galeria: str = None


class EventOut(Schema):
    id: int
    valor_cobrado: float
    quitado: bool
    status: EventStatus
    cliente_id: int
    cliente: PersonOut
    event_type_id: int
    gratuito: bool
    url_galeria: str = None
    cancelation_reason: int = None
    agendado_para: datetime = None