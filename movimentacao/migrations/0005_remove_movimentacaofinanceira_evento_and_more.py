# Generated by Django 4.0.3 on 2022-03-28 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movimentacao', '0004_evento_created_at_evento_updated_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movimentacaofinanceira',
            name='evento',
        ),
        migrations.RemoveField(
            model_name='movimentacaofinanceira',
            name='forma_pagamento',
        ),
        migrations.DeleteModel(
            name='Evento',
        ),
        migrations.DeleteModel(
            name='MotivoCancelamento',
        ),
        migrations.DeleteModel(
            name='MovimentacaoFinanceira',
        ),
        migrations.DeleteModel(
            name='Pessoa',
        ),
        migrations.DeleteModel(
            name='TipoEvento',
        ),
    ]
