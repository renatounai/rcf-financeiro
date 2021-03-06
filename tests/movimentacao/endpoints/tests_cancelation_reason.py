from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from ninja.errors import ValidationError

from apps.financial_transaction.endpoints.cancelation_reason_rest import CancelationReasonIn
from apps.financial_transaction.exceptions.FinancialTransactionError import FinancialTransactionError
from apps.financial_transaction.messages import MOTIVO_CANCELAMENTO_DESCRICAO_OBRIGATORIO, MOTIVO_CANCELAMENTO_DESCRICAO_REPETIDA
from apps.financial_transaction.models.cancelation_reason import CancelationReason

APPLICATION_JSON = "application/json"


class CancelationReasonTest(TestCase):

    def setUp(self):
        self.client.defaults["HTTP_AUTHORIZATION"] = "Bearer 123"

    def test_should_get_all_cancelation_reasons(self):
        CancelationReason.objects.create(description="Não tem dinheiro")
        CancelationReason.objects.create(description="Não gostou das fotos")

        response = self.client.get("/api/cancelation_reasons/")
        formas = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(formas), 2)

        self.assertEqual(formas[0]["description"], "Não tem dinheiro")
        self.assertEqual(formas[1]["description"], "Não gostou das fotos")

    def test_shoud_return_empty_if_nothing_found(self):
        response = self.client.get("/api/cancelation_reasons/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_shoud_get_a_tipo_de_event(self):
        cancelation_reason = CancelationReason.objects.create(description="Não tem dinheiro")

        response = self.client.get(f"/api/cancelation_reasons/{cancelation_reason.id}")

        forma_de_pagamento = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(forma_de_pagamento["description"], "Não tem dinheiro")

    def test_should_create_a_forma_de_pagamento(self):
        pix = CancelationReasonIn(description="Pix")

        response = self.client.post("/api/cancelation_reasons/", pix.__dict__, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CancelationReason.objects.count(), 1)

    def test_shoud_raise_error_when_missing_description(self):
        response = self.client.post("/api/cancelation_reasons/", {"description": ""}, content_type="application/json")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"], MOTIVO_CANCELAMENTO_DESCRICAO_OBRIGATORIO)

    def test_shoud_raise_error_when_description_is_white_space(self):
        response = self.client.post("/api/cancelation_reasons/", {"description": "   "}, content_type="application/json")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"], MOTIVO_CANCELAMENTO_DESCRICAO_OBRIGATORIO)

    def test_shoud_raise_error_when_description_is_null(self):
        response = self.client.post("/api/cancelation_reasons/", {"description": None}, content_type="application/json")
        self.assertEqual(response.status_code, 422)

    def test_shoud_update_a_forma_de_pagamento(self):
        cancelation_reason = CancelationReason.objects.create(description="Não tem dinheiro")

        response = self.client.put(f"/api/cancelation_reasons/{cancelation_reason.id}", {"description": "falta grana"},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        cancelation_reason = CancelationReason.objects.get(pk=cancelation_reason.id)

        self.assertEqual(cancelation_reason.description, "falta grana")

    def test_shoud_update_a_forma_de_pagamento_changing_case(self):
        cancelation_reason = CancelationReason.objects.create(description="Sem dinheiro")

        response = self.client.put(f"/api/cancelation_reasons/{cancelation_reason.id}", {"description": "sem dinheiro"},
                                   content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 200)
        cancelation_reason = CancelationReason.objects.get(pk=cancelation_reason.id)

        self.assertEqual(cancelation_reason.description, "sem dinheiro")

    def test_shoud_delete_a_forma_de_pagamento(self):
        cancelation_reason = CancelationReason.objects.create(description="Sem dinheiro")

        response = self.client.delete(f"/api/cancelation_reasons/{cancelation_reason.id}")
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(ObjectDoesNotExist):
            CancelationReason.objects.get(pk=1)

    def test_repeated_description(self):
        CancelationReason.objects.create(description="Sem dinheiro")
        with self.assertRaises(FinancialTransactionError, msg=MOTIVO_CANCELAMENTO_DESCRICAO_REPETIDA):
            CancelationReason(description="Sem dinheiro").save()

    def test_repeated_description_on_update(self):
        CancelationReason.objects.create(description="Sem dinheiro")
        viajou = CancelationReason.objects.create(description="Viajou")

        with self.assertRaises(FinancialTransactionError, msg=MOTIVO_CANCELAMENTO_DESCRICAO_REPETIDA):
            viajou.description = "Sem dinheiro"
            viajou.save()
