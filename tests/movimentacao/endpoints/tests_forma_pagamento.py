from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from ninja.errors import ValidationError

from movimentacao.endpoints.forma_pagamento_rest import FormaPagamentoIn
from movimentacao.exceptions.MovimentacaoError import MovimentacaoError
from movimentacao.messages import FORMA_PAGAMENTO_DESCRICAO_REPETIDA, FORMA_PAGAMENTO_DESCRICAO_OBRIGATORIA, \
    EVENTO_NOT_FOUND
from movimentacao.models.evento import Evento
from movimentacao.models.forma_pagamento import FormaPagamento

APPLICATION_JSON = "application/json"


class FormaPagamentoTest(TestCase):

    def test_should_get_all_formas_pagamento(self):
        FormaPagamento.objects.create(descricao="Pix")
        FormaPagamento.objects.create(descricao="Dinheiro")

        response = self.client.get("/api/formas_pagamento/")
        formas = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(formas), 2)

        self.assertEqual(formas[0]["descricao"], "Pix")
        self.assertEqual(formas[1]["descricao"], "Dinheiro")

    def test_shoud_return_empty_if_nothing_found(self):
        response = self.client.get("/api/formas_pagamento/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_shoud_get_a_forma_de_pagamento(self):
        forma_pagamento = FormaPagamento.objects.create(descricao="Pix")

        response = self.client.get(f"/api/formas_pagamento/{forma_pagamento.id}")

        forma_de_pagamento = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(forma_de_pagamento["descricao"], "Pix")

    def test_should_create_a_forma_de_pagamento(self):
        pix = FormaPagamentoIn(descricao="Pix")

        response = self.client.post("/api/formas_pagamento/", pix.__dict__, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FormaPagamento.objects.count(), 1)

    def test_shoud_raise_error_when_missing_description(self):
        response = self.client.post("/api/formas_pagamento/", {"descricao": ""}, content_type="application/json")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(FORMA_PAGAMENTO_DESCRICAO_OBRIGATORIA, response.json()["detail"])

    def test_shoud_raise_error_when_description_is_white_space(self):
        response = self.client.post("/api/formas_pagamento/", {"descricao": "     "}, content_type="application/json")
        self.assertEqual(422, response.status_code)

    def test_shoud_raise_error_when_description_is_null(self):
        response = self.client.post("/api/formas_pagamento/", {"descricao": None}, content_type="application/json")
        self.assertEqual(response.status_code, 422)

    def test_shoud_update_a_forma_de_pagamento(self):
        forma_pagamento = FormaPagamento.objects.create(descricao="Pix")

        response = self.client.put(f"/api/formas_pagamento/{forma_pagamento.id}", {"descricao": "Dinheiro"},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        forma_pagamento = FormaPagamento.objects.get(pk=forma_pagamento.id)

        self.assertEqual(forma_pagamento.descricao, "Dinheiro")

    def test_shoud_update_a_forma_de_pagamento_changing_case(self):
        forma_pagamento = FormaPagamento.objects.create(descricao="Pix")

        response = self.client.put(f"/api/formas_pagamento/{forma_pagamento.id}", {"descricao": "pix"},
                                   content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 200)
        forma_pagamento = FormaPagamento.objects.get(pk=forma_pagamento.id)

        self.assertEqual(forma_pagamento.descricao, "pix")

    def test_shoud_delete_a_forma_de_pagamento(self):
        forma_pagamento = FormaPagamento.objects.create(descricao="Pix")

        response = self.client.delete(f"/api/formas_pagamento/{forma_pagamento.id}")
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(ObjectDoesNotExist):
            FormaPagamento.objects.get(pk=1)

    def test_repeated_description(self):
        FormaPagamento(descricao="Pix").save()
        with self.assertRaises(ValidationError, msg=FORMA_PAGAMENTO_DESCRICAO_REPETIDA):
            FormaPagamento(descricao="Pix").save()

    def test_repeated_description_on_update(self):
        FormaPagamento.objects.create(descricao="Pix")
        dinheiro = FormaPagamento.objects.create(descricao="Dinheiro")

        with self.assertRaises(ValidationError, msg=FORMA_PAGAMENTO_DESCRICAO_REPETIDA):
            dinheiro.descricao = "Pix"
            dinheiro.save()

    def test_get_evento_not_exists(self):
        with self.assertRaises(MovimentacaoError, msg=EVENTO_NOT_FOUND):
            Evento.get(1)
