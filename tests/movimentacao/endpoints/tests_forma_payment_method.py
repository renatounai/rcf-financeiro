from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from ninja.errors import ValidationError

from apps.financial_transaction.endpoints.payment_method_rest import PaymentMethodIn
from apps.financial_transaction.exceptions.FinancialTransactionError import FinancialTransactionError
from apps.financial_transaction.messages import FORMA_PAGAMENTO_DESCRICAO_REPETIDA, FORMA_PAGAMENTO_DESCRICAO_OBRIGATORIA, \
    EVENTO_NOT_FOUND
from apps.financial_transaction.models.event import Event
from apps.financial_transaction.models.payment_method import PaymentMethod

APPLICATION_JSON = "application/json"


class PaymentMethodTest(TestCase):

    def setUp(self):
        self.client.defaults["HTTP_AUTHORIZATION"] = "Bearer 123"

    def test_should_get_all_payment_methods(self):
        PaymentMethod.objects.create(description="Pix")
        PaymentMethod.objects.create(description="Dinheiro")

        response = self.client.get("/api/payment_methods/")
        formas = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(formas), 2)

        self.assertEqual(formas[0]["description"], "Pix")
        self.assertEqual(formas[1]["description"], "Dinheiro")

    def test_shoud_return_empty_if_nothing_found(self):
        response = self.client.get("/api/payment_methods/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_shoud_get_a_forma_de_pagamento(self):
        payment_method = PaymentMethod.objects.create(description="Pix")

        response = self.client.get(f"/api/payment_methods/{payment_method.id}")

        forma_de_pagamento = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(forma_de_pagamento["description"], "Pix")

    def test_should_create_a_forma_de_pagamento(self):
        pix = PaymentMethodIn(description="Pix")

        response = self.client.post("/api/payment_methods/", pix.__dict__, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PaymentMethod.objects.count(), 1)

    def test_shoud_raise_error_when_missing_description(self):
        response = self.client.post("/api/payment_methods/", {"description": ""}, content_type="application/json")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(FORMA_PAGAMENTO_DESCRICAO_OBRIGATORIA, response.json()["detail"])

    def test_shoud_raise_error_when_description_is_white_space(self):
        response = self.client.post("/api/payment_methods/", {"description": "     "}, content_type="application/json")
        self.assertEqual(422, response.status_code)

    def test_shoud_raise_error_when_description_is_null(self):
        response = self.client.post("/api/payment_methods/", {"description": None}, content_type="application/json")
        self.assertEqual(response.status_code, 422)

    def test_shoud_update_a_forma_de_pagamento(self):
        payment_method = PaymentMethod.objects.create(description="Pix")

        response = self.client.put(f"/api/payment_methods/{payment_method.id}", {"description": "Dinheiro"},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        payment_method = PaymentMethod.objects.get(pk=payment_method.id)

        self.assertEqual(payment_method.description, "Dinheiro")

    def test_shoud_update_a_forma_de_pagamento_changing_case(self):
        payment_method = PaymentMethod.objects.create(description="Pix")

        response = self.client.put(f"/api/payment_methods/{payment_method.id}", {"description": "pix"},
                                   content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 200)
        payment_method = PaymentMethod.objects.get(pk=payment_method.id)

        self.assertEqual(payment_method.description, "pix")

    def test_shoud_delete_a_forma_de_pagamento(self):
        payment_method = PaymentMethod.objects.create(description="Pix")

        response = self.client.delete(f"/api/payment_methods/{payment_method.id}")
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(ObjectDoesNotExist):
            PaymentMethod.objects.get(pk=1)

    def test_repeated_description(self):
        PaymentMethod(description="Pix").save()
        with self.assertRaises(FinancialTransactionError, msg=FORMA_PAGAMENTO_DESCRICAO_REPETIDA):
            PaymentMethod(description="Pix").save()

    def test_repeated_description_on_update(self):
        PaymentMethod.objects.create(description="Pix")
        dinheiro = PaymentMethod.objects.create(description="Dinheiro")

        with self.assertRaises(FinancialTransactionError, msg=FORMA_PAGAMENTO_DESCRICAO_REPETIDA):
            dinheiro.description = "Pix"
            dinheiro.save()

    def test_get_event_not_exists(self):
        with self.assertRaises(FinancialTransactionError, msg=EVENTO_NOT_FOUND):
            Event.get(1)
