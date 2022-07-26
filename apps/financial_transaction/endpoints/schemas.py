from ninja import Schema
from pydantic import EmailStr
from pydantic.schema import datetime

from apps.financial_transaction.models.event_status import EventStatus
from apps.financial_transaction.models.financial_transaction_type import FinancialTransactionType


class EventTypeOut(Schema):
    id: int
    description: str


class EventTypeIn(Schema):
    description: str


class CancelationReasonOut(Schema):
    id: int
    description: str


class CancelationReasonIn(Schema):
    description: str


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
    amount: float
    date: datetime
    financial_transaction_type: FinancialTransactionType


class FinancialTransactionIn(Schema):
    event_id: int
    payment_method_id: int
    amount: float
    financial_transaction_type: FinancialTransactionType
    date: datetime = None


class PaymentMethodOut(Schema):
    id: int
    description: str


class PaymentMethodIn(Schema):
    description: str


class PersonOut(Schema):
    id: int
    name: str
    email: EmailStr = None
    phone: str = None
    instagram_user: str = None
    facebook_user: str = None


class PersonIn(Schema):
    name: str
    email: EmailStr = None
    phone: str = None
    instagram_user: str = None
    facebook_user: str = None


class EventIn(Schema):
    amount_charged: float = None
    paid: bool
    status: EventStatus
    clients_id: int
    cancelation_reason_id: int = None
    event_type_id: int
    scheduled_to: datetime = None
    gallery_url: str = None


class EventOut(Schema):
    id: int
    amount_charged: float
    paid: bool
    status: EventStatus
    clients_id: int
    clients: PersonOut
    event_type_id: int
    gallery_url: str = None
    cancelation_reason: int = None
    scheduled_to: datetime = None