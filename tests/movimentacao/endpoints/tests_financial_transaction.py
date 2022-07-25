from datetime import datetime
from decimal import Decimal
from time import timezone

from django.test import TestCase
from django.utils import timezone
from pydantic.datetime_parse import timezone

from apps.financial_transaction.endpoints.financial_transaction_rest import FinancialTransactionIn
from apps.financial_transaction.exceptions.FinancialTransactionError import FinancialTransactionError
from apps.financial_transaction.messages import MOVIMENTACAO_FINANCEIRA_EVENTO_OBRIGATORIO, \
    MOVIMENTACAO_FINANCEIRA_FORMA_PAGAMENTO_OBRIGATORIO, MOVIMENTACAO_FINANCEIRA_VALOR_OBRIGATORIO, \
    MOVIMENTACAO_FINANCEIRA_VALOR_NEGATIVO, MOVIMENTACAO_FINANCEIRA_TIPO_LANCAMENTO_OBRIGATORIO
from apps.financial_transaction.models.event import Event
from apps.financial_transaction.models.event_type import EventType
from apps.financial_transaction.models.financial_transaction import FinancialTransaction
from apps.financial_transaction.models.financial_transaction_type import FinancialTransactionType
from apps.financial_transaction.models.payment_method import PaymentMethod
from apps.financial_transaction.models.person import Person

JSON_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

APPLICATION_JSON = "application/json"


class FinancialTransactionTest(TestCase):
    event: Event
    pix: PaymentMethod

    @classmethod
    def setUpTestData(cls):
        person = Person(nome="Renato")
        person.save()

        event_type = EventType(descricao="Boudoir")
        event_type.save()

        cls.event = Event(cliente=person, event_type=event_type)
        cls.event.save()

        payment_method = PaymentMethod(descricao="Pix")
        payment_method.save()
        cls.pix = payment_method

    def test_should_get_all_financial_transactions(self):
        now = datetime.now(tz=timezone.utc)
        FinancialTransaction.objects.create(
            event=FinancialTransactionTest.event,
            payment_method=FinancialTransactionTest.pix,
            valor=Decimal("150.85"),
            financial_transaction_type=FinancialTransactionType.CREDIT,
            data_lancamento=now
        )

        FinancialTransaction.objects.create(
            event=FinancialTransactionTest.event,
            payment_method=FinancialTransactionTest.pix,
            valor=Decimal("30.40"),
            financial_transaction_type=FinancialTransactionType.DEBIT,
            data_lancamento=now
        )

        response = self.client.get("/api/financial_transactions/")
        formas = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(formas), 2)

        self.assertEqual(formas[0]["event_id"], FinancialTransactionTest.event.id)
        self.assertEqual(formas[0]["payment_method_id"], FinancialTransactionTest.pix.id)
        self.assertEqual(formas[0]["valor"], 150.85)
        self.assertEqual(formas[0]["financial_transaction_type"], FinancialTransactionType.CREDIT)
        self.assertEqual(formas[0]["data_lancamento"][:22], now.isoformat()[:22])

        self.assertEqual(formas[1]["event_id"], FinancialTransactionTest.event.id)
        self.assertEqual(formas[1]["payment_method_id"], FinancialTransactionTest.pix.id)
        self.assertEqual(formas[1]["valor"], 30.40)
        self.assertEqual(formas[1]["financial_transaction_type"], FinancialTransactionType.DEBIT)
        self.assertEqual(formas[1]["data_lancamento"][:22], now.isoformat()[:22])

    def test_shoud_return_empty_if_nothing_found(self):
        response = self.client.get("/api/financial_transactions/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_shoud_get_a_financial_transaction(self):
        data_lancamento = datetime.now(tz=timezone.utc)
        financial_transaction = FinancialTransaction.objects.create(
            event=FinancialTransactionTest.event,
            payment_method=FinancialTransactionTest.pix,
            valor=200.0,
            financial_transaction_type=FinancialTransactionType.CREDIT,
            data_lancamento=data_lancamento
        )

        response = self.client.get(f"/api/financial_transactions/{financial_transaction.id}")

        financial_transaction_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(financial_transaction_json["event_id"], FinancialTransactionTest.event.id)
        self.assertEqual(financial_transaction_json["payment_method_id"], FinancialTransactionTest.pix.id)
        self.assertEqual(financial_transaction_json["valor"], 200.0)
        self.assertEqual(financial_transaction_json["financial_transaction_type"], FinancialTransactionType.CREDIT)
        self.assertEqual(financial_transaction_json["data_lancamento"][:22], data_lancamento.isoformat()[:22])

    def test_should_create_a_financial_transaction_sem_data(self):
        financial_transaction_credito_sem_data_lancamento = FinancialTransactionIn(
            event_id=FinancialTransactionTest.event.id,
            payment_method_id=FinancialTransactionTest.pix.id,
            financial_transaction_type=FinancialTransactionType.CREDIT,
            valor=250.0
        )

        response = self.client.post(
            "/api/financial_transactions/",
            financial_transaction_credito_sem_data_lancamento.__dict__,
            content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(FinancialTransaction.objects.count(), 1)

    def test_should_create_a_financial_transaction_com_data(self):
        data_lancamento = datetime.now(tz=timezone.utc)
        financial_transaction_credito_sem_data_lancamento = FinancialTransactionIn(
            event_id=FinancialTransactionTest.event.id,
            payment_method_id=FinancialTransactionTest.pix.id,
            financial_transaction_type=FinancialTransactionType.CREDIT,
            valor=250.0,
            data_lancamento=data_lancamento
        )

        response = self.client.post(
            "/api/financial_transactions/",
            financial_transaction_credito_sem_data_lancamento.__dict__,
            content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(FinancialTransaction.objects.count(), 1)
        self.assertEqual(response.json()["data_lancamento"][:22], data_lancamento.isoformat()[:22])

    def test_should_raise_error_invalid_event(self):
        data_lancamento = datetime.now(tz=timezone.utc)
        financial_transaction_credito_sem_data_lancamento = FinancialTransactionIn(
            event_id=100,
            payment_method_id=FinancialTransactionTest.pix.id,
            financial_transaction_type=FinancialTransactionType.CREDIT,
            valor=250.0,
            data_lancamento=data_lancamento
        )

        response = self.client.post(
            "/api/financial_transactions/",
            financial_transaction_credito_sem_data_lancamento.__dict__,
            content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertTrue("A instância de event com id 100 não existe." in response.json()["detail"])

    def test_should_update_a_financial_transaction(self):
        financial_transaction = FinancialTransaction.objects.create(
            event=FinancialTransactionTest.event,
            payment_method=FinancialTransactionTest.pix,
            valor=200.0,
            financial_transaction_type=FinancialTransactionType.CREDIT,
            data_lancamento=datetime.now(tz=timezone.utc)
        )

        response = self.client.put(
            f"/api/financial_transactions/{financial_transaction.id}",
            {
                "event_id": financial_transaction.event_id,
                "payment_method_id": financial_transaction.payment_method_id,
                "valor": 320.50,
                "financial_transaction_type": financial_transaction.financial_transaction_type,
                "data_lancamento": financial_transaction.data_lancamento.isoformat()
            },
            content_type="application/json")

        self.assertEqual(200, response.status_code)
        updated_financial_transaction = FinancialTransaction.objects.get(pk=financial_transaction.id)
        self.assertEqual(updated_financial_transaction.valor, 320.50)

    def test_should_delete_a_financial_transaction(self):
        financial_transaction = FinancialTransaction.objects.create(
            event=FinancialTransactionTest.event,
            payment_method=FinancialTransactionTest.pix,
            valor=200.0,
            financial_transaction_type=FinancialTransactionType.CREDIT,
            data_lancamento=datetime.now(tz=timezone.utc)
        )

        response = self.client.delete(f"/api/financial_transactions/{financial_transaction.id}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, FinancialTransaction.objects.count())

    def test_shoud_raise_error_if_missing_event(self):
        financial_transaction = FinancialTransaction()

        with self.assertRaises(FinancialTransactionError, msg=MOVIMENTACAO_FINANCEIRA_EVENTO_OBRIGATORIO):
            financial_transaction.save()

    def test_shoud_raise_error_if_missing_payment_method(self):
        financial_transaction = FinancialTransaction(event_id=1)

        with self.assertRaises(FinancialTransactionError, msg=MOVIMENTACAO_FINANCEIRA_FORMA_PAGAMENTO_OBRIGATORIO):
            financial_transaction.save()

    def test_shoud_raise_error_if_missing_valor(self):
        financial_transaction = FinancialTransaction(event_id=1, payment_method_id=1)

        with self.assertRaises(FinancialTransactionError, msg=MOVIMENTACAO_FINANCEIRA_VALOR_OBRIGATORIO):
            financial_transaction.save()

    def test_shoud_raise_error_if_valor_is_zero(self):
        financial_transaction = FinancialTransaction(event_id=1, payment_method_id=1, valor=0)

        with self.assertRaises(FinancialTransactionError, msg=MOVIMENTACAO_FINANCEIRA_VALOR_OBRIGATORIO):
            financial_transaction.save()

    def test_shoud_raise_error_if_valor_is_less_than_zero(self):
        financial_transaction = FinancialTransaction(event_id=1, payment_method_id=1, valor=-10)

        with self.assertRaises(FinancialTransactionError, msg=MOVIMENTACAO_FINANCEIRA_VALOR_NEGATIVO):
            financial_transaction.save()

    def test_shoud_raise_error_if_missing_financial_transaction_type(self):
        financial_transaction = FinancialTransaction(event_id=1, payment_method_id=1, valor=10)

        with self.assertRaises(FinancialTransactionError, msg=MOVIMENTACAO_FINANCEIRA_TIPO_LANCAMENTO_OBRIGATORIO):
            financial_transaction.save()
