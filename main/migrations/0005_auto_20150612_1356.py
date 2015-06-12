# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20150612_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='personne',
            name='societe',
            field=models.CharField(blank=True, null=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='batiment',
            name='boite',
            field=models.CharField(blank=True, null=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='contrat',
            name='charges_base',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='contrat',
            name='loyer_base',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='fraismaintenance',
            name='entrepreneur',
            field=models.ForeignKey(null=True, blank=True, to='main.Personne'),
        ),
        migrations.AlterField(
            model_name='fraismaintenance',
            name='montant',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='location',
            name='charges',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='location',
            name='date_debut',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='location',
            name='loyer',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
