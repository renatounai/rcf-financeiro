from django.contrib import admin

from apps.financial_transaction.models.cancelation_reason import CancelationReason
from apps.financial_transaction.models.event import Event
from apps.financial_transaction.models.event_type import EventType
from apps.financial_transaction.models.financial_transaction import FinancialTransaction
from apps.financial_transaction.models.payment_method import PaymentMethod
from apps.financial_transaction.models.person import Person


admin.site.register(PaymentMethod)
admin.site.register(CancelationReason)
admin.site.register(EventType)
admin.site.register(Person)
admin.site.register(Event)
admin.site.register(FinancialTransaction)

