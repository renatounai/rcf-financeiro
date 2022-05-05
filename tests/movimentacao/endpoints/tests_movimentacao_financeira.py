from datetime import datetime

from django.test import TestCase

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
    def setUpClass(cls):
        pessoa = Pessoa(nome="Renato")
        pessoa.save()

        tipo_evento = TipoEvento(descricao="Boudoir")
        tipo_evento.save()

        cls.evento = Evento(cliente=pessoa, tipo_evento=tipo_evento)
        cls.evento.save()

        forma_pagamento = FormaPagamento(descricao="Pix")
        forma_pagamento.save()
        cls.pix = forma_pagamento

        super().setUpClass()

    def test_should_get_all_movimentacao_financeiras(self):

        MovimentacaoFinanceira.objects.create(
            evento=MovimentacaoFinanceiraTest.evento,
            forma_pagamento=MovimentacaoFinanceiraTest.pix,
            valor=150.85,
            tipo_lancamento=TipoLancamento.CREDITO
        )

        MovimentacaoFinanceira.objects.create(
            evento=MovimentacaoFinanceiraTest.evento,
            forma_pagamento=MovimentacaoFinanceiraTest.pix,
            valor=30.40,
            tipo_lancamento=TipoLancamento.DEBITO
        )

        response = self.client.get("/api/movimentacoes_financeiras/")
        formas = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(formas), 2)

        self.assertEqual(formas[0]["evento_id"], MovimentacaoFinanceiraTest.evento.id)
        self.assertEqual(formas[0]["forma_pagamento_id"], MovimentacaoFinanceiraTest.pix.id)
        self.assertEqual(formas[0]["valor"], 150.85)
        self.assertEqual(formas[0]["tipo_lancamento"], TipoLancamento.CREDITO)
        data_lancamento = datetime.strptime(formas[0]["data_lancamento"], JSON_DATETIME_FORMAT)
        self.assertEqual(data_lancamento.date(), datetime.today().date())

        self.assertEqual(formas[1]["evento_id"], MovimentacaoFinanceiraTest.evento.id)
        self.assertEqual(formas[1]["forma_pagamento_id"], MovimentacaoFinanceiraTest.pix.id)
        self.assertEqual(formas[1]["valor"], 30.40)
        self.assertEqual(formas[1]["tipo_lancamento"], TipoLancamento.DEBITO)
        data_lancamento = datetime.strptime(formas[1]["data_lancamento"], JSON_DATETIME_FORMAT)
        self.assertEqual(data_lancamento.date(), datetime.today().date())
