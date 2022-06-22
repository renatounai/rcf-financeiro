from datetime import datetime
from decimal import Decimal
from time import timezone

from django.test import TestCase
from django.utils import timezone
from pydantic.datetime_parse import timezone

from movimentacao.endpoints.movimentacao_financeira_rest import MovimentacaoFinanceiraIn
from movimentacao.exceptions.MovimentacaoError import MovimentacaoError
from movimentacao.messages import MOVIMENTACAO_FINANCEIRA_EVENTO_OBRIGATORIO, \
    MOVIMENTACAO_FINANCEIRA_FORMA_PAGAMENTO_OBRIGATORIO, MOVIMENTACAO_FINANCEIRA_VALOR_OBRIGATORIO, \
    MOVIMENTACAO_FINANCEIRA_VALOR_NEGATIVO, MOVIMENTACAO_FINANCEIRA_TIPO_LANCAMENTO_OBRIGATORIO
from movimentacao.models.evento import Evento
from movimentacao.models.forma_pagamento import FormaPagamento
from movimentacao.models.movimentacao_financeira import MovimentacaoFinanceira
from movimentacao.models.pessoa import Pessoa
from movimentacao.models.tipo_evento import TipoEvento
from movimentacao.models.tipo_lancamento import TipoLancamento

JSON_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

APPLICATION_JSON = "application/json"


class MovimentacaoFinanceiraTest(TestCase):
    evento: Evento
    pix: FormaPagamento

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

        now = datetime.now(tz=timezone.utc)
        MovimentacaoFinanceira.objects.create(
            evento=MovimentacaoFinanceiraTest.evento,
            forma_pagamento=MovimentacaoFinanceiraTest.pix,
            valor=Decimal("150.85"),
            tipo_lancamento=TipoLancamento.CREDITO,
            data_lancamento=now
        )

        MovimentacaoFinanceira.objects.create(
            evento=MovimentacaoFinanceiraTest.evento,
            forma_pagamento=MovimentacaoFinanceiraTest.pix,
            valor=Decimal("30.40"),
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
        self.assertEqual(formas[0]["data_lancamento"][:22], now.isoformat()[:22])

        self.assertEqual(formas[1]["evento_id"], MovimentacaoFinanceiraTest.evento.id)
        self.assertEqual(formas[1]["forma_pagamento_id"], MovimentacaoFinanceiraTest.pix.id)
        self.assertEqual(formas[1]["valor"], 30.40)
        self.assertEqual(formas[1]["tipo_lancamento"], TipoLancamento.DEBITO)
        self.assertEqual(formas[1]["data_lancamento"][:22], now.isoformat()[:22])

    def test_shoud_return_empty_if_nothing_found(self):
        response = self.client.get("/api/movimentacoes_financeiras/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_shoud_get_a_movimentacao_financeira(self):
        data_lancamento = datetime.now(tz=timezone.utc)
        movimentacao_financeira = MovimentacaoFinanceira.objects.create(
            evento=MovimentacaoFinanceiraTest.evento,
            forma_pagamento=MovimentacaoFinanceiraTest.pix,
            valor=200.0,
            tipo_lancamento=TipoLancamento.CREDITO,
            data_lancamento=data_lancamento
        )

        response = self.client.get(f"/api/movimentacoes_financeiras/{movimentacao_financeira.id}")

        movimentacao_financeira_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(movimentacao_financeira_json["evento_id"], MovimentacaoFinanceiraTest.evento.id)
        self.assertEqual(movimentacao_financeira_json["forma_pagamento_id"], MovimentacaoFinanceiraTest.pix.id)
        self.assertEqual(movimentacao_financeira_json["valor"], 200.0)
        self.assertEqual(movimentacao_financeira_json["tipo_lancamento"], TipoLancamento.CREDITO)
        self.assertEqual(movimentacao_financeira_json["data_lancamento"][:22], data_lancamento.isoformat()[:22])

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
        data_lancamento = datetime.now(tz=timezone.utc)
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
        self.assertEqual(response.json()["data_lancamento"][:22], data_lancamento.isoformat()[:22])

    def test_should_raise_error_invalid_event(self):
        data_lancamento = datetime.now(tz=timezone.utc)
        movimentacao_financeira_credito_sem_data_lancamento = MovimentacaoFinanceiraIn(
            evento_id=100,
            forma_pagamento_id=MovimentacaoFinanceiraTest.pix.id,
            tipo_lancamento=TipoLancamento.CREDITO,
            valor=250.0,
            data_lancamento=data_lancamento
        )

        response = self.client.post(
            "/api/movimentacoes_financeiras/",
            movimentacao_financeira_credito_sem_data_lancamento.__dict__,
            content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], ["A instância de evento com id 100 não existe."])

    def test_should_update_a_movimentacao_financeira(self):
        movimentacao_financeira = MovimentacaoFinanceira.objects.create(
            evento=MovimentacaoFinanceiraTest.evento,
            forma_pagamento=MovimentacaoFinanceiraTest.pix,
            valor=200.0,
            tipo_lancamento=TipoLancamento.CREDITO,
            data_lancamento=datetime.now(tz=timezone.utc)
        )

        response = self.client.put(
            f"/api/movimentacoes_financeiras/{movimentacao_financeira.id}",
            {
                "evento_id": movimentacao_financeira.evento_id,
                "forma_pagamento_id": movimentacao_financeira.forma_pagamento_id,
                "valor": 320.50,
                "tipo_lancamento": movimentacao_financeira.tipo_lancamento,
                "data_lancamento": movimentacao_financeira.data_lancamento.isoformat()
            },
            content_type="application/json")

        self.assertEqual(200, response.status_code)
        updated_movimentacao_financeira = MovimentacaoFinanceira.objects.get(pk=movimentacao_financeira.id)
        self.assertEqual(updated_movimentacao_financeira.valor, 320.50)

    def test_should_delete_a_movimentacao_financeira(self):
        movimentacao_financeira = MovimentacaoFinanceira.objects.create(
            evento=MovimentacaoFinanceiraTest.evento,
            forma_pagamento=MovimentacaoFinanceiraTest.pix,
            valor=200.0,
            tipo_lancamento=TipoLancamento.CREDITO,
            data_lancamento=datetime.now(tz=timezone.utc)
        )

        response = self.client.delete(f"/api/movimentacoes_financeiras/{movimentacao_financeira.id}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, MovimentacaoFinanceira.objects.count())

    def test_shoud_raise_error_if_missing_evento(self):
        movimentacao_financeira = MovimentacaoFinanceira()

        with self.assertRaises(MovimentacaoError, msg=MOVIMENTACAO_FINANCEIRA_EVENTO_OBRIGATORIO):
            movimentacao_financeira.save()

    def test_shoud_raise_error_if_missing_forma_pagamento(self):
        movimentacao_financeira = MovimentacaoFinanceira(evento_id=1)

        with self.assertRaises(MovimentacaoError, msg=MOVIMENTACAO_FINANCEIRA_FORMA_PAGAMENTO_OBRIGATORIO):
            movimentacao_financeira.save()

    def test_shoud_raise_error_if_missing_valor(self):
        movimentacao_financeira = MovimentacaoFinanceira(evento_id=1, forma_pagamento_id=1)

        with self.assertRaises(MovimentacaoError, msg=MOVIMENTACAO_FINANCEIRA_VALOR_OBRIGATORIO):
            movimentacao_financeira.save()

    def test_shoud_raise_error_if_valor_is_zero(self):
        movimentacao_financeira = MovimentacaoFinanceira(evento_id=1, forma_pagamento_id=1, valor=0)

        with self.assertRaises(MovimentacaoError, msg=MOVIMENTACAO_FINANCEIRA_VALOR_OBRIGATORIO):
            movimentacao_financeira.save()

    def test_shoud_raise_error_if_valor_is_less_than_zero(self):
        movimentacao_financeira = MovimentacaoFinanceira(evento_id=1, forma_pagamento_id=1, valor=-10)

        with self.assertRaises(MovimentacaoError, msg=MOVIMENTACAO_FINANCEIRA_VALOR_NEGATIVO):
            movimentacao_financeira.save()

    def test_shoud_raise_error_if_missing_tipo_lancamento(self):
        movimentacao_financeira = MovimentacaoFinanceira(evento_id=1, forma_pagamento_id=1, valor=10)

        with self.assertRaises(MovimentacaoError, msg=MOVIMENTACAO_FINANCEIRA_TIPO_LANCAMENTO_OBRIGATORIO):
            movimentacao_financeira.save()
