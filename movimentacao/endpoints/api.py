from django.core.exceptions import ValidationError
from ninja import NinjaAPI

from auth.auth import router as auth_router
from auth.auth_bearer import AuthBearer
from auth.user_rest import router as users_router
from financeiro import settings
from movimentacao.endpoints.cancelation_reason_rest import router as cancelation_reasons_router
from movimentacao.endpoints.event_rest import router as events_router
from movimentacao.endpoints.event_type_rest import router as event_types_router
from movimentacao.endpoints.financial_transaction_rest import router as financial_transaction_router
from movimentacao.endpoints.payment_method_rest import router as payment_methods_router
from movimentacao.endpoints.person_rest import router as persons_router

auth = None if settings.TESTING else AuthBearer()
api = NinjaAPI(auth=auth)


@api.exception_handler(ValidationError)
def validation_errors(request, exc):
    return api.create_response(
        request,
        {"detail": exc.messages},
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
