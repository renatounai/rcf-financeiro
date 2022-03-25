from django.db import models


class FormaPagamento(models.Model):
    descricao = models.CharField(max_length=30)

    def __str__(self):
        return self.descricao


class MovimentacaoFinanceira(models.Model):
    descricao = models.CharField(max_length=200)
    agendado_para = models.DateTimeField()
    valor_cobrado = models.DecimalField(max_digits=9, decimal_places=2, null=True)

    def __str__(self):
        return self.descricao


class ItemMovimentacao(models.Model):
    CREDITO = 'C'
    DEBITO = 'D'

    TIPO_LANCAMENTO = (
        (CREDITO, 'Crédito'),
        (DEBITO, 'Débito'),
    )

    movimentacao = models.ForeignKey(MovimentacaoFinanceira, on_delete=models.CASCADE)
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=9, decimal_places=2)
    data_lancamento = models.DateTimeField(auto_now=True)
    tipo_lancamento = models.CharField(max_length=1, choices=TIPO_LANCAMENTO, default=CREDITO)

    def __str__(self):
        return f'{self.movimentacao.descricao}, ' \
               f'{self.tipo_lancamento} ' \
               f'{self.valor} no ' \
               f'{self.forma_pagamento} em ' \
               f'{self.data_lancamento}'
