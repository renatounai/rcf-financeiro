from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from movimentacao.endpoints.tipo_evento_rest import TipoEventoIn
from movimentacao.exceptions.movimentacao_error import MovimentacaoError
from movimentacao.messages import TIPO_EVENTO_DESCRICAO_REPETIDA, \
    TIPO_EVENTO_DESCRICAO_OBRIGATORIO
from movimentacao.models.tipo_evento import TipoEvento

APPLICATION_JSON = "application/json"


class TipoEventoTest(TestCase):

    def test_should_get_all_tipos_evento(self):
        TipoEvento.objects.create(descricao="Boudoir")
        TipoEvento.objects.create(descricao="Gestante")

        response = self.client.get("/api/tipos_evento")
        formas = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(formas), 2)

        self.assertEqual(formas[0]["descricao"], "Boudoir")
        self.assertEqual(formas[1]["descricao"], "Gestante")

    def test_shoud_return_204_if_nothing_found(self):
        response = self.client.get("/api/tipos_evento")
        self.assertEqual(response.status_code, 204)

    def test_shoud_get_a_tipo_de_evento(self):
        tipo_evento = TipoEvento.objects.create(descricao="Boudoir")

        response = self.client.get(f"/api/tipos_evento/{tipo_evento.id}")

        forma_de_pagamento = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(forma_de_pagamento["descricao"], "Boudoir")

    def test_should_create_a_forma_de_pagamento(self):
        pix = TipoEventoIn(descricao="Pix")

        response = self.client.post("/api/tipos_evento", pix.__dict__, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(TipoEvento.objects.count(), 1)

    def test_shoud_raise_error_when_missing_description(self):
        response = self.client.post("/api/tipos_evento", {"descricao": ""}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], TIPO_EVENTO_DESCRICAO_OBRIGATORIO)

    def test_shoud_raise_error_when_description_is_white_space(self):
        response = self.client.post("/api/tipos_evento", {"descricao": "     "}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], TIPO_EVENTO_DESCRICAO_OBRIGATORIO)

    def test_shoud_raise_error_when_description_is_null(self):
        response = self.client.post("/api/tipos_evento", {"descricao": None}, content_type="application/json")
        self.assertEqual(response.status_code, 422)

    def test_shoud_update_a_forma_de_pagamento(self):
        tipo_evento = TipoEvento.objects.create(descricao="Boudoir")

        response = self.client.put(f"/api/tipos_evento/{tipo_evento.id}", {"descricao": "Gestante"},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        tipo_evento = TipoEvento.objects.get(pk=tipo_evento.id)

        self.assertEqual(tipo_evento.descricao, "Gestante")

    def test_shoud_update_a_forma_de_pagamento_changing_case(self):
        tipo_evento = TipoEvento.objects.create(descricao="Boudoir")

        response = self.client.put(f"/api/tipos_evento/{tipo_evento.id}", {"descricao": "boudoir"},
                                   content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 200)
        tipo_evento = TipoEvento.objects.get(pk=tipo_evento.id)

        self.assertEqual(tipo_evento.descricao, "boudoir")

    def test_shoud_delete_a_forma_de_pagamento(self):
        tipo_evento = TipoEvento.objects.create(descricao="Boudoir")

        response = self.client.delete(f"/api/tipos_evento/{tipo_evento.id}")
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(ObjectDoesNotExist):
            TipoEvento.objects.get(pk=1)

    def test_repeated_description(self):
        TipoEvento.objects.create(descricao="Boudoir")
        with self.assertRaises(MovimentacaoError, msg=TIPO_EVENTO_DESCRICAO_REPETIDA):
            TipoEvento.objects.create(descricao="Boudoir")
