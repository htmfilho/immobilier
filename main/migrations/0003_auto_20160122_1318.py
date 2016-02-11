# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20160122_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alerte',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('description', models.TextField()),
                ('date_alerte', models.DateField(null=True, blank=True)),
                ('etat', models.CharField(max_length=10, choices=[('A_VERIFIER', 'A vérifier'), ('VERIFIER', 'Vérifier'), ('COURRIER', 'Courrier à préparer')], default='A_VERIFIER')),
                ('contratGestion', models.ForeignKey(null=True, blank=True, to='main.ContratGestion')),
                ('contratLocation', models.ForeignKey(null=True, blank=True, to='main.ContratLocation')),
            ],
        ),
        migrations.RemoveField(
            model_name='batiment',
            name='photo',
        ),
    ]
