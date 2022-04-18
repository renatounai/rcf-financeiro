from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from movimentacao.endpoints.pessoa_rest import PessoaIn
from movimentacao.models.evento import Evento
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

    def deve_lancar_erro_ao_informar_motivo_cancelamento_quando_nao_cancelado(self):
        pass