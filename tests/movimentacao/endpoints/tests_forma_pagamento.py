from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from movimentacao.endpoints.forma_pagamento_rest import FormaPagamentoIn
from movimentacao.exceptions.movimentacao_error import MovimentacaoError
from movimentacao.messages import JA_EXISTE_FORMA_PAGAMENTO_COM_ESTA_DESCRICAO, FORMA_PAGAMENTO_DESCRICAO_OBRIGATORIA
from movimentacao.models.forma_pagamento import FormaPagamento

API_PATH = "/api/formas_de_pagamento"

APPLICATION_JSON = "application/json"


class FormaPagamentoTest(TestCase):

    def test_should_get_all_formas_de_pagamento(self):
        FormaPagamento.objects.create(descricao="Pix")
        FormaPagamento.objects.create(descricao="Dinheiro")

        response = self.client.get(API_PATH)
        formas = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(formas), 2)

        self.assertEqual(formas[0]["descricao"], "Pix")
        self.assertEqual(formas[1]["descricao"], "Dinheiro")

    def test_shoud_return_204_if_nothing_found(self):
        response = self.client.get(API_PATH)
        self.assertEqual(response.status_code, 204)

    def test_shoud_get_a_forma_de_pagamento(self):
        forma_pagamento = FormaPagamento.objects.create(descricao="Pix")

        response = self.client.get(f"{API_PATH}/{forma_pagamento.id}")

        forma_de_pagamento = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(forma_de_pagamento["descricao"], "Pix")

    def test_should_create_a_forma_de_pagamento(self):
        pix = FormaPagamentoIn(descricao="Pix")

        response = self.client.post(API_PATH, pix.__dict__, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FormaPagamento.objects.count(), 1)

    def test_shoud_raise_error_when_missing_description(self):
        response = self.client.post(API_PATH, {"descricao": ""}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], FORMA_PAGAMENTO_DESCRICAO_OBRIGATORIA)

    def test_shoud_raise_error_when_description_is_white_space(self):
        response = self.client.post(API_PATH, {"descricao": "     "}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], FORMA_PAGAMENTO_DESCRICAO_OBRIGATORIA)

    def test_shoud_raise_error_when_description_is_null(self):
        response = self.client.post(API_PATH, {"descricao": None}, content_type="application/json")
        self.assertEqual(response.status_code, 422)

    def test_shoud_update_a_forma_de_pagamento(self):
        forma_pagamento = FormaPagamento.objects.create(descricao="Pix")

        response = self.client.put(f"{API_PATH}/{forma_pagamento.id}", {"descricao": "Dinheiro"},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        forma_pagamento = FormaPagamento.objects.get(pk=forma_pagamento.id)

        self.assertEqual(forma_pagamento.descricao, "Dinheiro")

    def test_shoud_update_a_forma_de_pagamento_changing_case(self):
        forma_pagamento = FormaPagamento.objects.create(descricao="Pix")

        response = self.client.put(f"{API_PATH}/{forma_pagamento.id}", {"descricao": "pix"},
                                   content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 200)
        forma_pagamento = FormaPagamento.objects.get(pk=forma_pagamento.id)

        self.assertEqual(forma_pagamento.descricao, "pix")

    def test_shoud_delete_a_forma_de_pagamento(self):
        forma_pagamento = FormaPagamento.objects.create(descricao="Pix")

        response = self.client.delete(f"{API_PATH}/{forma_pagamento.id}")
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(ObjectDoesNotExist):
            FormaPagamento.objects.get(pk=1)

    def test_repeated_description(self):
        FormaPagamento.objects.create(descricao="Pix")
        with self.assertRaises(MovimentacaoError, msg=JA_EXISTE_FORMA_PAGAMENTO_COM_ESTA_DESCRICAO):
            FormaPagamento.objects.create(descricao="Pix")
