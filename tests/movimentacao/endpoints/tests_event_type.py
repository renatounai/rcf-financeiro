from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from ninja.errors import ValidationError

from apps.financial_transaction.endpoints.event_type_rest import EventTypeIn
from apps.financial_transaction.exceptions.FinancialTransactionError import FinancialTransactionError
from apps.financial_transaction.messages import TIPO_EVENTO_DESCRICAO_REPETIDA, \
    TIPO_EVENTO_DESCRICAO_OBRIGATORIO
from apps.financial_transaction.models.event_type import EventType

APPLICATION_JSON = "application/json"


class EventTypeTest(TestCase):

    def test_should_get_all_event_types(self):
        EventType.objects.create(descricao="Boudoir")
        EventType.objects.create(descricao="Gestante")

        response = self.client.get("/api/event_types/")
        formas = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(formas), 2)

        self.assertEqual(formas[0]["descricao"], "Boudoir")
        self.assertEqual(formas[1]["descricao"], "Gestante")

    def test_shoud_return_empty_if_nothing_found(self):
        response = self.client.get("/api/event_types/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_shoud_get_a_tipo_de_event(self):
        event_type = EventType.objects.create(descricao="Boudoir")

        response = self.client.get(f"/api/event_types/{event_type.id}")

        forma_de_pagamento = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(forma_de_pagamento["descricao"], "Boudoir")

    def test_should_create_a_forma_de_pagamento(self):
        pix = EventTypeIn(descricao="Pix")

        response = self.client.post("/api/event_types/", pix.__dict__, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(EventType.objects.count(), 1)

    def test_shoud_raise_error_when_missing_description(self):
        response = self.client.post("/api/event_types/", {"descricao": ""}, content_type="application/json")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"], TIPO_EVENTO_DESCRICAO_OBRIGATORIO)

    def test_shoud_raise_error_when_description_is_white_space(self):
        response = self.client.post("/api/event_types/", {"descricao": "     "}, content_type="application/json")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"], TIPO_EVENTO_DESCRICAO_OBRIGATORIO)

    def test_shoud_raise_error_when_description_is_null(self):
        response = self.client.post("/api/event_types/", {"descricao": None}, content_type="application/json")
        self.assertEqual(response.status_code, 422)

    def test_shoud_update_a_forma_de_pagamento(self):
        event_type = EventType.objects.create(descricao="Boudoir")

        response = self.client.put(f"/api/event_types/{event_type.id}", {"descricao": "Gestante"},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        event_type = EventType.objects.get(pk=event_type.id)

        self.assertEqual(event_type.descricao, "Gestante")

    def test_shoud_update_a_forma_de_pagamento_changing_case(self):
        event_type = EventType.objects.create(descricao="Boudoir")

        response = self.client.put(f"/api/event_types/{event_type.id}", {"descricao": "boudoir"},
                                   content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 200)
        event_type = EventType.objects.get(pk=event_type.id)

        self.assertEqual(event_type.descricao, "boudoir")

    def test_shoud_delete_a_forma_de_pagamento(self):
        event_type = EventType.objects.create(descricao="Boudoir")

        response = self.client.delete(f"/api/event_types/{event_type.id}")
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(ObjectDoesNotExist):
            EventType.objects.get(pk=1)

    def test_repeated_description(self):
        EventType.objects.create(descricao="Boudoir")
        with self.assertRaises(FinancialTransactionError, msg=TIPO_EVENTO_DESCRICAO_REPETIDA):
            EventType(descricao="Boudoir").save()

    def test_repeated_description_on_update(self):
        EventType.objects.create(descricao="Boudoir")
        gestante = EventType.objects.create(descricao="Gestante")

        with self.assertRaises(FinancialTransactionError, msg=TIPO_EVENTO_DESCRICAO_REPETIDA):
            gestante.descricao = "Boudoir"
            gestante.save()
