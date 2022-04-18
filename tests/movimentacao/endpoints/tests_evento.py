from django.test import TestCase

from movimentacao.messages import EVENTO_MOTIVO_CANCELAMENTO_FORA_DO_STATUS_CANCELADO
from movimentacao.models.evento import Evento
from movimentacao.models.motivo_cancelamento import MotivoCancelamento
from movimentacao.models.pessoa import Pessoa
from movimentacao.models.status_evento import StatusEvento
from movimentacao.models.tipo_evento import TipoEvento

APPLICATION_JSON = "application/json"


class EventoTest(TestCase):

    def test_should_create_an_evento(self):
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

