# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-22 11:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_indicesante'),
    ]

    operations = [
        migrations.AddField(
            model_name='contratlocation',
            name='indice_sante_base',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.IndiceSante'),
        ),
        migrations.AddField(
            model_name='financementlocation',
            name='indice_sante',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.IndiceSante'),
        ),
        migrations.AlterUniqueTogether(
            name='indicesante',
            unique_together=set([('date_calcul', 'annee_base')]),
        ),
    ]
