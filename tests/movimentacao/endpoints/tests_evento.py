from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from movimentacao.endpoints.pessoa_rest import PessoaIn
from movimentacao.models.evento import Evento
from movimentacao.models.pessoa import Pessoa

APPLICATION_JSON = "application/json"


class EventoTest(TestCase):

    def test_should_get_all_eventos(self):
        response = self.client.get("/api/eventos/")
        self.assertEqual(response.status_code, 204)
