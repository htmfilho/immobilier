# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20160209_1019'),
    ]

    operations = [
        migrations.CreateModel(
            name='Honoraire',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('date_paiement', models.DateField(verbose_name='Date paiement', null=True, blank=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='alerte',
            options={'ordering': ['date_alerte']},
        ),
        migrations.AddField(
            model_name='contratgestion',
            name='montant_mensuel',
            field=models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='honoraire',
            name='contrat_gestion',
            field=models.ForeignKey(to='main.ContratGestion'),
        ),
    ]
