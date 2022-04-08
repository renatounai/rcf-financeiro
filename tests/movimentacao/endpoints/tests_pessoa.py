from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from movimentacao.endpoints.pessoa_rest import PessoaIn
from movimentacao.exceptions.movimentacao_error import MovimentacaoError
from movimentacao.messages import TIPO_EVENTO_DESCRICAO_REPETIDA, \
    TIPO_EVENTO_DESCRICAO_OBRIGATORIO
from movimentacao.models.pessoa import Pessoa

APPLICATION_JSON = "application/json"


class PessoaTest(TestCase):

    def test_should_get_all_pessoas(self):
        Pessoa.objects.create(nome="Renato")
        Pessoa.objects.create(nome="Ellen")

        response = self.client.get("/api/pessoas")
        formas = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(formas), 2)

        self.assertEqual(formas[0]["nome"], "Renato")
        self.assertEqual(formas[1]["nome"], "Ellen")

