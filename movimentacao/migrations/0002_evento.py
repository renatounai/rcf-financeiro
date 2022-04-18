# Generated by Django 4.0.4 on 2022-04-13 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movimentacao', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('agendado_para', models.DateTimeField(null=True)),
                ('valor_cobrado', models.DecimalField(decimal_places=2, max_digits=9, null=True)),
                ('quitado', models.BooleanField(default=False)),
                ('status', models.IntegerField(choices=[(1, 'Negociando'), (2, 'Agendado'), (3, 'Realizado'), (4, 'Em escolha'), (5, 'Em tratamento'), (6, 'Entregue'), (7, 'Cancelado')], default=1)),
                ('url_galeria', models.URLField()),
                ('gratuito', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movimentacao.pessoa')),
                ('motivo_cancelamento', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='movimentacao.motivocancelamento')),
                ('tipo_evento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='movimentacao.tipoevento')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]