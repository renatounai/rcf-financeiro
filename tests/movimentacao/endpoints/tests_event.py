import datetime

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

    def setUp(self):
        self.client.defaults["HTTP_AUTHORIZATION"] = "Bearer 123"

    def test_should_create_an_event(self):
        person = Person(name="Renato")
        person.save()

        event_type = EventType(description="Boudoir")
        event_type.save()

        event_in = {
            "paid": False,
            "status": EventStatus.NEGOTIATING,
            "clients_id": person.id,
            "event_type_id": event_type.id,
            "amount_charged": 100.00,
        }

        response = self.client.post("/api/events/", event_in, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 201)

    def test_deve_lancar_erro_ao_informar_cancelation_reason_quando_nao_cancelado(self):
        person = Person(name="Renato")
        person.save()

        event_type = EventType(description="Boudoir")
        event_type.save()

        cancelation_reason = CancelationReason(description="Não tem dinheiro")
        cancelation_reason.save()

        event_in = {
            "paid": False,
            "status": EventStatus.NEGOTIATING,
            "clients_id": person.id,
            "event_type_id": event_type.id,
            "cancelation_reason_id": cancelation_reason.id
        }

        response = self.client.post("/api/events/", event_in, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()['detail'], EVENTO_MOTIVO_CANCELAMENTO_FORA_DO_STATUS_CANCELED)

    def test_deve_cancelar_event(self):
        event = Event(paid=False, status=EventStatus.NEGOTIATING,
                      clients=Person.objects.create(name="Renato"),
                      event_type=EventType.objects.create(description="Boudoir"))
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
        event = Event(paid=False, status=EventStatus.NEGOTIATING,
                      clients=Person.objects.create(name="Renato"),
                      event_type=EventType.objects.create(description="Boudoir"))
        event.save()

        cancelation_reason = CancelationReason(description="Falta de dinheiro")
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
        renato = Person(name="Renato")
        renato.save()

        ellen = Person(name="Ellen")
        ellen.save()

        event_type = EventType(description="Boudoir")
        event_type.save()

        Event.objects.create(
            scheduled_to=datetime.datetime(2022, 6, 20, 16, tzinfo=timezone.utc),
            amount_charged=300.0,
            paid=False,
            status=EventStatus.NEGOTIATING,
            clients=renato,
            event_type=event_type
        )

        Event.objects.create(
            scheduled_to=datetime.datetime(2022, 7, 20, 20, 30, tzinfo=timezone.utc),
            amount_charged=0,
            paid=False,
            status=EventStatus.NEGOTIATING,
            clients=ellen,
            event_type=event_type,
            gallery_url="https://site.com"
        )

        response = self.client.get("/api/events/")
        events = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]["amount_charged"], 300.0)
        self.assertEqual(events[0]["scheduled_to"], '2022-06-20T16:00:00Z')
        self.assertEqual(events[0]["paid"], False)
        self.assertEqual(events[0]["status"], EventStatus.NEGOTIATING)
        self.assertIsNone(events[0]["gallery_url"])
        self.assertEqual(events[0]["clients"]["name"], "Renato")
        self.assertEqual(events[0]["event_type_id"], event_type.id)

        self.assertEqual(events[1]["amount_charged"], 0)
        self.assertEqual(events[1]["scheduled_to"], '2022-07-20T20:30:00Z')
        self.assertEqual(events[1]["paid"], False)
        self.assertEqual(events[1]["status"], EventStatus.NEGOTIATING)
        self.assertEqual(events[1]["clients"]["name"], "Ellen")
        self.assertEqual(events[1]["gallery_url"], "https://site.com")
        self.assertEqual(events[1]["event_type_id"], event_type.id)

    def test_should_get_an_event(self):
        renato = Person(name="Renato")
        renato.save()

        event_type = EventType(description="Boudoir")
        event_type.save()

        event_saved = Event.objects.create(
            scheduled_to=datetime.datetime(2022, 6, 20, 16, tzinfo=timezone.utc),
            amount_charged=300.0,
            paid=False,
            status=EventStatus.NEGOTIATING,
            clients=renato,
            event_type=event_type
        )

        response = self.client.get(f"/api/events/{event_saved.id}")

        event = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(event["id"], event_saved.id)
        self.assertEqual(event["scheduled_to"], '2022-06-20T16:00:00Z')
        self.assertEqual(event["paid"], False)
        self.assertEqual(event["status"], EventStatus.NEGOTIATING)
        self.assertIsNone(event["gallery_url"])
        self.assertEqual(event["clients"]["name"], "Renato")
        self.assertEqual(event["event_type_id"], event_type.id)

    def test_should_update_an_event(self):
        renato = Person(name="Renato")
        renato.save()

        event_type = EventType(description="Boudoir")
        event_type.save()

        event_type_casamento = EventType(description="Casamento")
        event_type_casamento.save()

        event_saved = Event.objects.create(
            scheduled_to=datetime.datetime(2022, 6, 20, 16, tzinfo=timezone.utc),
            amount_charged=300.0,
            paid=False,
            status=EventStatus.NEGOTIATING,
            clients=renato,
            event_type=event_type
        )

        event_in = {
            "paid": event_saved.paid,
            "status": event_saved.status,
            "clients_id": event_saved.clients_id,
            "amount_charged": event_saved.amount_charged,
            "event_type_id": event_type_casamento.id,
        }

        response = self.client.put(f"/api/events/{event_saved.id}", event_in,
                                   content_type="application/json")

        event = Event.objects.get(pk=event_saved.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(event.id, event_saved.id)
        self.assertEqual(event.event_type_id, event_type_casamento.id)
