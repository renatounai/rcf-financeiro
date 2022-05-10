from datetime import datetime
from time import timezone

from django.test import TestCase
from django.utils import timezone

from movimentacao.endpoints.movimentacao_financeira_rest import MovimentacaoFinanceiraIn
from movimentacao.models.evento import Evento
from movimentacao.models.forma_pagamento import FormaPagamento
from movimentacao.models.movimentacao_financeira import MovimentacaoFinanceira
from movimentacao.models.pessoa import Pessoa
from movimentacao.models.tipo_evento import TipoEvento
from movimentacao.models.tipo_lancamento import TipoLancamento

JSON_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

APPLICATION_JSON = "application/json"


class MovimentacaoFinanceiraTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        pessoa = Pessoa(nome="Renato")
        pessoa.save()

        tipo_evento = TipoEvento(descricao="Boudoir")
        tipo_evento.save()

        cls.evento = Evento(cliente=pessoa, tipo_evento=tipo_evento)
        cls.evento.save()

        forma_pagamento = FormaPagamento(descricao="Pix")
        forma_pagamento.save()
        cls.pix = forma_pagamento

    def test_should_get_all_movimentacao_financeiras(self):

        now = timezone.now()
        MovimentacaoFinanceira.objects.create(
            evento=MovimentacaoFinanceiraTest.evento,
            forma_pagamento=MovimentacaoFinanceiraTest.pix,
            valor=150.85,
            tipo_lancamento=TipoLancamento.CREDITO,
            data_lancamento=now
        )

        MovimentacaoFinanceira.objects.create(
            evento=MovimentacaoFinanceiraTest.evento,
            forma_pagamento=MovimentacaoFinanceiraTest.pix,
            valor=30.40,
            tipo_lancamento=TipoLancamento.DEBITO,
            data_lancamento=now
        )

        response = self.client.get("/api/movimentacoes_financeiras/")
        formas = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(formas), 2)

        self.assertEqual(formas[0]["evento_id"], MovimentacaoFinanceiraTest.evento.id)
        self.assertEqual(formas[0]["forma_pagamento_id"], MovimentacaoFinanceiraTest.pix.id)
        self.assertEqual(formas[0]["valor"], 150.85)
        self.assertEqual(formas[0]["tipo_lancamento"], TipoLancamento.CREDITO)
        self.assertEqual(formas[0]["data_lancamento"], now)

        self.assertEqual(formas[1]["evento_id"], MovimentacaoFinanceiraTest.evento.id)
        self.assertEqual(formas[1]["forma_pagamento_id"], MovimentacaoFinanceiraTest.pix.id)
        self.assertEqual(formas[1]["valor"], 30.40)
        self.assertEqual(formas[1]["tipo_lancamento"], TipoLancamento.DEBITO)
        self.assertEqual(formas[1]["data_lancamento"], now)

    def test_shoud_return_empty_if_nothing_found(self):
        response = self.client.get("/api/movimentacoes_financeiras/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_shoud_get_a_movimentacao_financeira(self):
        now = timezone.now()
        movimentacao_financeira = MovimentacaoFinanceira.objects.create(
            evento=MovimentacaoFinanceiraTest.evento,
            forma_pagamento=MovimentacaoFinanceiraTest.pix,
            valor=200.0,
            tipo_lancamento=TipoLancamento.CREDITO,
            data_lancamento=now
        )

        response = self.client.get(f"/api/movimentacoes_financeiras/{movimentacao_financeira.id}")

        movimentacao_financeira_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(movimentacao_financeira_json["evento_id"], movimentacao_financeira.id)
        self.assertEqual(movimentacao_financeira_json["forma_pagamento_id"], MovimentacaoFinanceiraTest.pix.id)
        self.assertEqual(movimentacao_financeira_json["valor"], 200.0)
        self.assertEqual(movimentacao_financeira_json["tipo_lancamento"], TipoLancamento.CREDITO)
        self.assertEqual(movimentacao_financeira_json["data_lancamento"], now)

    def test_should_create_a_movimentacao_financeira_sem_data(self):
        movimentacao_financeira_credito_sem_data_lancamento = MovimentacaoFinanceiraIn(
            evento_id=MovimentacaoFinanceiraTest.evento.id,
            forma_pagamento_id=MovimentacaoFinanceiraTest.pix.id,
            tipo_lancamento=TipoLancamento.CREDITO,
            valor=250.0
        )

        response = self.client.post(
            "/api/movimentacoes_financeiras/",
            movimentacao_financeira_credito_sem_data_lancamento.__dict__,
            content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(MovimentacaoFinanceira.objects.count(), 1)

    def test_should_create_a_movimentacao_financeira_com_data(self):
        data_lancamento = timezone.timezone(2022, 5, 10, 11, 50, 30, 0)
        movimentacao_financeira_credito_sem_data_lancamento = MovimentacaoFinanceiraIn(
            evento_id=MovimentacaoFinanceiraTest.evento.id,
            forma_pagamento_id=MovimentacaoFinanceiraTest.pix.id,
            tipo_lancamento=TipoLancamento.CREDITO,
            valor=250.0,
            data_lancamento=data_lancamento
        )

        response = self.client.post(
            "/api/movimentacoes_financeiras/",
            movimentacao_financeira_credito_sem_data_lancamento.__dict__,
            content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(MovimentacaoFinanceira.objects.count(), 1)
        self.assertEqual(response.json()["data_lancamento"], data_lancamento.isoformat())
