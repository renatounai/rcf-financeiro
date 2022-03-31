from django.test import TestCase
import json

from .endpoints.forma_pagamento_rest import FormaPagamentoIn
from .models.forma_pagamento import FormaPagamento


class FormaPagamentoTest(TestCase):

    def test_should_get_all_formas_de_pagamento(self):
        FormaPagamento(descricao="Pix").save()
        FormaPagamento(descricao="Dinheiro").save()

        response = self.client.get("/api/formas_de_pagamento")
        formas = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(formas), 2)

        self.assertEqual(formas[0]["descricao"], "Pix")
        self.assertEqual(formas[1]["descricao"], "Dinheiro")

    def test_shoud_get_a_forma_de_pagamento(self):
        FormaPagamento(descricao="Pix").save()
        response = self.client.get("/api/formas_de_pagamento/1")
        forma_de_pagamento = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(forma_de_pagamento["descricao"], "Pix")

    def test_should_create_a_forma_de_pagamento(self):
        pix = FormaPagamentoIn(descricao="Pix")

        response = self.client.post("/api/formas_de_pagamento", pix.__dict__, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FormaPagamento.objects.count(), 1)


