from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from ninja.errors import ValidationError

from movimentacao.endpoints.motivo_cancelamento_rest import MotivoCancelamentoIn
from movimentacao.messages import TIPO_EVENTO_DESCRICAO_REPETIDA, \
    MOTIVO_CANCELAMENTO_DESCRICAO_OBRIGATORIO, MOTIVO_CANCELAMENTO_DESCRICAO_REPETIDA
from movimentacao.models.motivo_cancelamento import MotivoCancelamento
from movimentacao.services import motivo_cancelamento_service

APPLICATION_JSON = "application/json"


class MotivoCancelamentoTest(TestCase):

    def test_should_get_all_motivos_cancelamento(self):
        MotivoCancelamento.objects.create(descricao="Não tem dinheiro")
        MotivoCancelamento.objects.create(descricao="Não gostou das fotos")

        response = self.client.get("/api/motivos_cancelamento/")
        formas = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(formas), 2)

        self.assertEqual(formas[0]["descricao"], "Não tem dinheiro")
        self.assertEqual(formas[1]["descricao"], "Não gostou das fotos")

    def test_shoud_return_empty_if_nothing_found(self):
        response = self.client.get("/api/motivos_cancelamento/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_shoud_get_a_tipo_de_evento(self):
        motivo_cancelamento = MotivoCancelamento.objects.create(descricao="Não tem dinheiro")

        response = self.client.get(f"/api/motivos_cancelamento/{motivo_cancelamento.id}")

        forma_de_pagamento = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(forma_de_pagamento["descricao"], "Não tem dinheiro")

    def test_should_create_a_forma_de_pagamento(self):
        pix = MotivoCancelamentoIn(descricao="Pix")

        response = self.client.post("/api/motivos_cancelamento/", pix.__dict__, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(MotivoCancelamento.objects.count(), 1)

    def test_shoud_raise_error_when_missing_description(self):
        response = self.client.post("/api/motivos_cancelamento/", {"descricao": ""}, content_type="application/json")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"], MOTIVO_CANCELAMENTO_DESCRICAO_OBRIGATORIO)

    def test_shoud_raise_error_when_description_is_white_space(self):
        response = self.client.post("/api/motivos_cancelamento/", {"descricao": "    "}, content_type="application/json")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"], MOTIVO_CANCELAMENTO_DESCRICAO_OBRIGATORIO)

    def test_shoud_raise_error_when_description_is_null(self):
        response = self.client.post("/api/motivos_cancelamento/", {"descricao": None}, content_type="application/json")
        self.assertEqual(response.status_code, 422)

    def test_shoud_update_a_forma_de_pagamento(self):
        motivo_cancelamento = MotivoCancelamento.objects.create(descricao="Não tem dinheiro")

        response = self.client.put(f"/api/motivos_cancelamento/{motivo_cancelamento.id}", {"descricao": "falta grana"},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        motivo_cancelamento = MotivoCancelamento.objects.get(pk=motivo_cancelamento.id)

        self.assertEqual(motivo_cancelamento.descricao, "falta grana")

    def test_shoud_update_a_forma_de_pagamento_changing_case(self):
        motivo_cancelamento = MotivoCancelamento.objects.create(descricao="Sem dinheiro")

        response = self.client.put(f"/api/motivos_cancelamento/{motivo_cancelamento.id}", {"descricao": "sem dinheiro"},
                                   content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 200)
        motivo_cancelamento = MotivoCancelamento.objects.get(pk=motivo_cancelamento.id)

        self.assertEqual(motivo_cancelamento.descricao, "sem dinheiro")

    def test_shoud_delete_a_forma_de_pagamento(self):
        motivo_cancelamento = MotivoCancelamento.objects.create(descricao="Sem dinheiro")

        response = self.client.delete(f"/api/motivos_cancelamento/{motivo_cancelamento.id}")
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(ObjectDoesNotExist):
            MotivoCancelamento.objects.get(pk=1)

    def test_repeated_description(self):
        MotivoCancelamento.objects.create(descricao="Sem dinheiro")
        with self.assertRaises(ValidationError, msg=MOTIVO_CANCELAMENTO_DESCRICAO_REPETIDA):
            motivo_cancelamento_service.save(MotivoCancelamento(descricao="Sem dinheiro"))

    def test_repeated_description_on_update(self):
        MotivoCancelamento.objects.create(descricao="Sem dinheiro")
        viajou = MotivoCancelamento.objects.create(descricao="Viajou")

        with self.assertRaises(ValidationError, msg=MOTIVO_CANCELAMENTO_DESCRICAO_REPETIDA):
            viajou.descricao = "Sem dinheiro"
            motivo_cancelamento_service.save(viajou)
