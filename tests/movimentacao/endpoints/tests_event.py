import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.financial_transaction.messages import EVENTO_MOTIVO_CANCELAMENTO_FORA_DO_STATUS_CANCELED
from apps.financial_transaction.models.cancelation_reason import CancelationReason
from apps.financial_transaction.models.event import Event
from apps.financial_transaction.models.event_status import EventStatus
from apps.financial_transaction.models.event_type import EventType
from apps.financial_transaction.models.person import Person

APPLICATION_JSON = "application/json"


class EventTest(TestCase):

    def test_should_create_an_event(self):
        user_model = get_user_model()
        user_model.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')

        person = Person(nome="Renato")
        person.save()

        event_type = EventType(descricao="Boudoir")
        event_type.save()

        event_in = {
            "quitado": False,
            "gratuito": False,
            "status": EventStatus.NEGOTIATING,
            "cliente_id": person.id,
            "event_type_id": event_type.id,
            "valor_cobrado": 100.00,
        }

        response = self.client.post("/api/events/", event_in, content_type=APPLICATION_JSON)
        print(response.json())
        self.assertEqual(response.status_code, 201)

    def test_deve_lancar_erro_ao_informar_cancelation_reason_quando_nao_cancelado(self):
        person = Person(nome="Renato")
        person.save()

        event_type = EventType(descricao="Boudoir")
        event_type.save()

        cancelation_reason = CancelationReason(descricao="Não tem dinheiro")
        cancelation_reason.save()

        event_in = {
            "quitado": False,
            "status": EventStatus.NEGOTIATING,
            "gratuito": False,
            "cliente_id": person.id,
            "event_type_id": event_type.id,
            "cancelation_reason_id": cancelation_reason.id
        }

        response = self.client.post("/api/events/", event_in, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()['detail'], EVENTO_MOTIVO_CANCELAMENTO_FORA_DO_STATUS_CANCELED)

    def test_deve_cancelar_event(self):
        event = Event(quitado=False, status=EventStatus.NEGOTIATING, gratuito=False,
                      cliente=Person.objects.create(nome="Renato"),
                      event_type=EventType.objects.create(descricao="Boudoir"))
        event.save()

        cancelamento_in = {
            "id": None,
            "description": "Falta de dinheiro"
        }

        response = self.client.put(f"/api/events/cancelar/{event.id}", cancelamento_in, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 204)
        event = Event.objects.get(id=event.id)
        self.assertTrue(EventStatus.CANCELED, event.status)

    def test_deve_cancelar_event_with_cancelation_reason(self):
        event = Event(quitado=False, status=EventStatus.NEGOTIATING, gratuito=False,
                      cliente=Person.objects.create(nome="Renato"),
                      event_type=EventType.objects.create(descricao="Boudoir"))
        event.save()

        cancelation_reason = CancelationReason(descricao="Falta de dinheiro")
        cancelation_reason.save()

        cancelamento_in = {
            "id": cancelation_reason.id,
            "description": None
        }

        response = self.client.put(f"/api/events/cancelar/{event.id}", cancelamento_in, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 204)
        event = Event.objects.get(id=event.id)
        self.assertTrue(EventStatus.CANCELED, event.status)

    def test_shoud_get_all_events(self):
        renato = Person(nome="Renato")
        renato.save()

        ellen = Person(nome="Ellen")
        ellen.save()

        event_type = EventType(descricao="Boudoir")
        event_type.save()

        Event.objects.create(
            agendado_para=datetime.datetime(2022, 6, 20, 16, tzinfo=timezone.utc),
            valor_cobrado=300.0,
            quitado=False,
            status=EventStatus.NEGOTIATING,
            cliente=renato,
            event_type=event_type,
            gratuito=False
        )

        Event.objects.create(
            agendado_para=datetime.datetime(2022, 7, 20, 20, 30, tzinfo=timezone.utc),
            valor_cobrado=0,
            quitado=False,
            status=EventStatus.NEGOTIATING,
            cliente=ellen,
            event_type=event_type,
            gratuito=True,
            url_galeria="https://site.com"
        )

        response = self.client.get("/api/events/")
        events = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]["valor_cobrado"], 300.0)
        self.assertEqual(events[0]["agendado_para"], '2022-06-20T16:00:00Z')
        self.assertEqual(events[0]["quitado"], False)
        self.assertEqual(events[0]["status"], EventStatus.NEGOTIATING)
        self.assertIsNone(events[0]["url_galeria"])
        self.assertEqual(events[0]["cliente"]["nome"], "Renato")
        self.assertEqual(events[0]["event_type_id"], event_type.id)

        self.assertEqual(events[1]["valor_cobrado"], 0)
        self.assertEqual(events[1]["agendado_para"], '2022-07-20T20:30:00Z')
        self.assertEqual(events[1]["quitado"], False)
        self.assertEqual(events[1]["status"], EventStatus.NEGOTIATING)
        self.assertEqual(events[1]["cliente"]["nome"], "Ellen")
        self.assertEqual(events[1]["url_galeria"], "https://site.com")
        self.assertEqual(events[1]["event_type_id"], event_type.id)

    def test_should_get_an_event(self):
        renato = Person(nome="Renato")
        renato.save()

        event_type = EventType(descricao="Boudoir")
        event_type.save()

        event_saved = Event.objects.create(
            agendado_para=datetime.datetime(2022, 6, 20, 16, tzinfo=timezone.utc),
            valor_cobrado=300.0,
            quitado=False,
            status=EventStatus.NEGOTIATING,
            cliente=renato,
            event_type=event_type,
            gratuito=False
        )

        response = self.client.get(f"/api/events/{event_saved.id}")

        event = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(event["id"], event_saved.id)
        self.assertEqual(event["agendado_para"], '2022-06-20T16:00:00Z')
        self.assertEqual(event["quitado"], False)
        self.assertEqual(event["status"], EventStatus.NEGOTIATING)
        self.assertIsNone(event["url_galeria"])
        self.assertEqual(event["cliente"]["nome"], "Renato")
        self.assertEqual(event["event_type_id"], event_type.id)

    def test_should_update_an_event(self):
        renato = Person(nome="Renato")
        renato.save()

        event_type = EventType(descricao="Boudoir")
        event_type.save()

        event_type_casamento = EventType(descricao="Casamento")
        event_type_casamento.save()

        event_saved = Event.objects.create(
            agendado_para=datetime.datetime(2022, 6, 20, 16, tzinfo=timezone.utc),
            valor_cobrado=300.0,
            quitado=False,
            status=EventStatus.NEGOTIATING,
            cliente=renato,
            event_type=event_type,
            gratuito=False
        )

        event_in = {
            "quitado": event_saved.quitado,
            "status": event_saved.status,
            "gratuito": event_saved.gratuito,
            "cliente_id": event_saved.cliente_id,
            "valor_cobrado": event_saved.valor_cobrado,
            "event_type_id": event_type_casamento.id,
        }

        response = self.client.put(f"/api/events/{event_saved.id}", event_in,
                                   content_type="application/json")

        event = Event.objects.get(pk=event_saved.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(event.id, event_saved.id)
        self.assertEqual(event.event_type_id, event_type_casamento.id)
