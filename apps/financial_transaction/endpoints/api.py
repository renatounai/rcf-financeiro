from ninja import NinjaAPI

from django.core.exceptions import ValidationError

from apps.financial_transaction.auth.auth import router as auth_router
from apps.financial_transaction.auth.auth_bearer import AuthBearer
from apps.financial_transaction.auth.user_rest import router as users_router
from apps.financial_transaction.endpoints.cancelation_reason_rest import router as cancelation_reasons_router
from apps.financial_transaction.endpoints.event_rest import router as events_router
from apps.financial_transaction.endpoints.event_type_rest import router as event_types_router
from apps.financial_transaction.endpoints.financial_transaction_rest import router as financial_transaction_router
from apps.financial_transaction.endpoints.payment_method_rest import router as payment_methods_router
from apps.financial_transaction.endpoints.person_rest import router as persons_router
from apps.financial_transaction.exceptions.FinancialTransactionError import FinancialTransactionError
from project import settings

auth = AuthBearer()
api = NinjaAPI(auth=auth)


@api.exception_handler(FinancialTransactionError)
def validation_custom_errors(request, exc):
    return api.create_response(
        request,
        {"detail": str(exc)},
        status=400,
    )


@api.exception_handler(ValidationError)
def validation_django_errors(request, exc):
    return api.create_response(
        request,
        {"detail": str(exc)},
        status=400,
    )


api.add_router("/payment_methods", payment_methods_router)
api.add_router("/cancelation_reasons", cancelation_reasons_router)
api.add_router("/persons", persons_router)
api.add_router("/event_types", event_types_router)
api.add_router("/events", events_router)
api.add_router("/financial_transactions", financial_transaction_router)
api.add_router("/auth", auth_router)
api.add_router("/users", users_router)

# payment_methods_router.api = api
