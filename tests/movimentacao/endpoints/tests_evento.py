import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from movimentacao.messages import EVENTO_MOTIVO_CANCELAMENTO_FORA_DO_STATUS_CANCELADO
from movimentacao.models.evento import Evento
from movimentacao.models.motivo_cancelamento import MotivoCancelamento
from movimentacao.models.pessoa import Pessoa
from movimentacao.models.status_evento import StatusEvento
from movimentacao.models.tipo_evento import TipoEvento

APPLICATION_JSON = "application/json"


class EventoTest(TestCase):

    def test_should_create_an_evento(self):
        user_model = get_user_model()
        user_model.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')

        pessoa = Pessoa(nome="Renato")
        pessoa.save()

        tipo_evento = TipoEvento(descricao="Boudoir")
        tipo_evento.save()

        evento_in = {
            "quitado": False,
            "status": StatusEvento.NEGOCIANDO,
            "gratuito": False,
            "cliente_id": pessoa.id,
            "tipo_evento_id": tipo_evento.id
        }

        response = self.client.post("/api/eventos/", evento_in, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 201)

    def test_should_create_an_evento_with_only_cliente_name(self):
        tipo_evento = TipoEvento(descricao="Boudoir")
        tipo_evento.save()

        evento_in = {
            "quitado": False,
            "status": StatusEvento.NEGOCIANDO,
            "gratuito": False,
            "cliente_nome": "Renato",
            "tipo_evento_id": tipo_evento.id
        }

        response = self.client.post("/api/eventos/", evento_in, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 201)
        self.assertTrue('Renato', response.json()["cliente"]["nome"])

    def test_should_create_an_evento_with_only_motivo_cancelamento_descricao(self):
        tipo_evento = TipoEvento(descricao="Boudoir")
        tipo_evento.save()

        pessoa = Pessoa(nome="Renato")
        pessoa.save()

        evento_in = {
            "quitado": False,
            "status": StatusEvento.CANCELADO,
            "gratuito": False,
            "cliente_id": pessoa.id,
            "tipo_evento_id": tipo_evento.id,
            "motivo_cancelamento_descricao": "Falta de dinheiro"
        }

        response = self.client.post("/api/eventos/", evento_in, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 201)

    def test_should_create_an_evento_with_only_tipo_evento_descricao(self):
        pessoa = Pessoa(nome="Renato")
        pessoa.save()

        evento_in = {
            "quitado": False,
            "status": StatusEvento.CANCELADO,
            "gratuito": False,
            "cliente_id": pessoa.id,
            "tipo_evento_descricao": 'Batizado',
            "motivo_cancelamento_descricao": "Falta de dinheiro"
        }

        response = self.client.post("/api/eventos/", evento_in, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 201)

    def test_deve_lancar_erro_ao_informar_motivo_cancelamento_quando_nao_cancelado(self):
        pessoa = Pessoa(nome="Renato")
        pessoa.save()

        tipo_evento = TipoEvento(descricao="Boudoir")
        tipo_evento.save()

        motivo_cancelamento = MotivoCancelamento(descricao="Não tem dinheiro")
        motivo_cancelamento.save()

        evento_in = {
            "quitado": False,
            "status": StatusEvento.NEGOCIANDO,
            "gratuito": False,
            "cliente_id": pessoa.id,
            "tipo_evento_id": tipo_evento.id,
            "motivo_cancelamento_id": motivo_cancelamento.id
        }

        response = self.client.post("/api/eventos/", evento_in, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()['detail'], EVENTO_MOTIVO_CANCELAMENTO_FORA_DO_STATUS_CANCELADO)

    def test_deve_cancelar_evento(self):
        evento = Evento(quitado=False, status=StatusEvento.NEGOCIANDO, gratuito=False,
                        cliente=Pessoa.objects.create(nome="Renato"),
                        tipo_evento=TipoEvento.objects.create(descricao="Boudoir"))
        evento.save()

        cancelamento_in = {
            "motivo_cancelamento_id": None,
            "motivo_cancelamento_descricao": "Falta de dinheiro"
        }

        response = self.client.put(f"/api/eventos/cancelar/{evento.id}", cancelamento_in, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 200)
        evento = Evento.objects.get(id=evento.id)
        self.assertTrue(StatusEvento.CANCELADO, evento.status)

    def test_deve_cancelar_evento_with_motivo_cancelamento(self):
        evento = Evento(quitado=False, status=StatusEvento.NEGOCIANDO, gratuito=False,
                        cliente=Pessoa.objects.create(nome="Renato"),
                        tipo_evento=TipoEvento.objects.create(descricao="Boudoir"))
        evento.save()

        motivo_cancelamento = MotivoCancelamento(descricao="Falta de dinheiro")
        motivo_cancelamento.save()

        cancelamento_in = {
            "motivo_cancelamento_id": motivo_cancelamento.id,
            "motivo_cancelamento_descricao": None
        }

        response = self.client.put(f"/api/eventos/cancelar/{evento.id}", cancelamento_in, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 200)
        evento = Evento.objects.get(id=evento.id)
        self.assertTrue(StatusEvento.CANCELADO, evento.status)

    def test_shoud_get_all_eventos(self):
        renato = Pessoa(nome="Renato")
        renato.save()

        ellen = Pessoa(nome="Ellen")
        ellen.save()

        tipo_evento = TipoEvento(descricao="Boudoir")
        tipo_evento.save()

        Evento.objects.create(
            agendado_para=datetime.datetime(2022, 6, 20, 16, tzinfo=timezone.utc),
            valor_cobrado=300.0,
            quitado=False,
            status=StatusEvento.NEGOCIANDO,
            cliente=renato,
            tipo_evento=tipo_evento,
            gratuito=False
        )

        Evento.objects.create(
            agendado_para=datetime.datetime(2022, 7, 20, 20, 30, tzinfo=timezone.utc),
            valor_cobrado=0,
            quitado=False,
            status=StatusEvento.NEGOCIANDO,
            cliente=ellen,
            tipo_evento=tipo_evento,
            gratuito=True,
            url_galeria="https://site.com"
        )

        response = self.client.get("/api/eventos/")
        eventos = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(eventos), 2)
        self.assertEqual(eventos[0]["valor_cobrado"], 300.0)
        self.assertEqual(eventos[0]["agendado_para"], '2022-06-20T16:00:00Z')
        self.assertEqual(eventos[0]["quitado"], False)
        self.assertEqual(eventos[0]["status"], StatusEvento.NEGOCIANDO)
        self.assertIsNone(eventos[0]["url_galeria"])
        self.assertEqual(eventos[0]["cliente"]["nome"], "Renato")
        self.assertEqual(eventos[0]["tipo_evento_id"], tipo_evento.id)

        self.assertEqual(eventos[1]["valor_cobrado"], 0)
        self.assertEqual(eventos[1]["agendado_para"], '2022-07-20T20:30:00Z')
        self.assertEqual(eventos[1]["quitado"], False)
        self.assertEqual(eventos[1]["status"], StatusEvento.NEGOCIANDO)
        self.assertEqual(eventos[1]["cliente"]["nome"], "Ellen")
        self.assertEqual(eventos[1]["url_galeria"], "https://site.com")
        self.assertEqual(eventos[1]["tipo_evento_id"], tipo_evento.id)

    def test_should_get_an_evento(self):
        renato = Pessoa(nome="Renato")
        renato.save()

        tipo_evento = TipoEvento(descricao="Boudoir")
        tipo_evento.save()

        evento_saved = Evento.objects.create(
            agendado_para=datetime.datetime(2022, 6, 20, 16, tzinfo=timezone.utc),
            valor_cobrado=300.0,
            quitado=False,
            status=StatusEvento.NEGOCIANDO,
            cliente=renato,
            tipo_evento=tipo_evento,
            gratuito=False
        )

        response = self.client.get(f"/api/eventos/{evento_saved.id}")

        evento = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(evento["id"], evento_saved.id)
        self.assertEqual(evento["agendado_para"], '2022-06-20T16:00:00Z')
        self.assertEqual(evento["quitado"], False)
        self.assertEqual(evento["status"], StatusEvento.NEGOCIANDO)
        self.assertIsNone(evento["url_galeria"])
        self.assertEqual(evento["cliente"]["nome"], "Renato")
        self.assertEqual(evento["tipo_evento_id"], tipo_evento.id)

    def test_should_update_an_evento(self):
        renato = Pessoa(nome="Renato")
        renato.save()

        tipo_evento = TipoEvento(descricao="Boudoir")
        tipo_evento.save()

        tipo_evento_casamento = TipoEvento(descricao="Casamento")
        tipo_evento_casamento.save()

        evento_saved = Evento.objects.create(
            agendado_para=datetime.datetime(2022, 6, 20, 16, tzinfo=timezone.utc),
            valor_cobrado=300.0,
            quitado=False,
            status=StatusEvento.NEGOCIANDO,
            cliente=renato,
            tipo_evento=tipo_evento,
            gratuito=False
        )

        evento_in = {
            "quitado": evento_saved.quitado,
            "status": evento_saved.status,
            "gratuito": evento_saved.gratuito,
            "cliente_id": evento_saved.cliente_id,
            "tipo_evento_id": tipo_evento_casamento.id,
            "motivo_cancelamento_id": evento_saved.motivo_cancelamento_id
        }

        response = self.client.put(f"/api/eventos/{evento_saved.id}", evento_in,
                                   content_type="application/json")

        evento = Evento.objects.get(pk=evento_saved.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(evento.id, evento_saved.id)
        self.assertEqual(evento.tipo_evento_id, tipo_evento_casamento.id)



