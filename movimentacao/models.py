from datetime import datetime

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class FormaPagamento(models.Model):
    descricao = models.CharField(max_length=30)

    def __str__(self):
        return self.descricao


class MotivoCancelamento(models.Model):
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return self.descricao


class Pessoa(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField()
    fone = PhoneNumberField()
    instagram_user = models.CharField(max_length=100)
    facebook_user = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class TipoEvento(models.Model):
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao


class Evento(models.Model):
    NEGOCIANDO = 1
    AGENDADO = 2
    REALIZADO = 3
    EM_ESCOLHA = 4
    EM_TRATAMENTO = 5
    ENTREGUE = 6
    CANCELADO = 7

    STATUS_EVENTO = (
        (NEGOCIANDO, 'Negociando'),
        (AGENDADO, 'Agendado'),
        (REALIZADO, 'Realizado'),
        (EM_ESCOLHA, 'Em escolha'),
        (EM_TRATAMENTO, 'Em tratamento'),
        (ENTREGUE, 'Entregue'),
        (CANCELADO, 'Cancelado'),
    )

    agendado_para = models.DateTimeField(null=True)
    valor_cobrado = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    quitado = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS_EVENTO, default=NEGOCIANDO)
    motivo_cancelamento = models.ForeignKey(MotivoCancelamento, on_delete=models.PROTECT, null=True)
    cliente = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.PROTECT)
    url_galeria = models.URLField()

    def agendar_para(self, horario_realizacao: datetime):
        if horario_realizacao is None:
            raise ValueError("O horário de realização do evento é obrigatório!")

        if self.status != Evento.NEGOCIANDO:
            raise ValueError("Só é possível agendar eventos que ainda estão em negociação")

        self.agendado_para = horario_realizacao
        self.status = Evento.AGENDADO

    def __str__(self):
        return f'{self.tipo_evento.descricao} {self.cliente.nome} {self.agendado_para}'


class MovimentacaoFinanceira(models.Model):
    CREDITO = 'C'
    DEBITO = 'D'

    TIPO_LANCAMENTO = (
        (CREDITO, 'Crédito'),
        (DEBITO, 'Débito'),
    )

    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=9, decimal_places=2)
    data_lancamento = models.DateTimeField(auto_now=True)
    tipo_lancamento = models.CharField(max_length=1, choices=TIPO_LANCAMENTO, default=CREDITO)

    def __str__(self):
        return f'{self.evento.tipo_evento.descricao} ' \
               f'{self.evento.cliente}, ' \
               f'{self.tipo_lancamento} ' \
               f'{self.valor} no ' \
               f'{self.forma_pagamento} em ' \
               f'{self.data_lancamento}'
