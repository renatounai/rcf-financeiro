# Generated by Django 4.0.4 on 2022-05-05 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movimentacao', '0004_alter_evento_motivo_cancelamento_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimentacaofinanceira',
            name='evento',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='movimentacao.evento'),
            preserve_default=False,
        ),
    ]
