# Generated by Django 4.0.3 on 2022-03-29 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimentacao', '0005_remove_movimentacaofinanceira_evento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formapagamento',
            name='descricao',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
