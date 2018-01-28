# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-09 16:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_professionnel_actif'),
    ]

    operations = [
        migrations.AddField(
            model_name='locataire',
            name='actif',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='proprietaire',
            name='actif',
            field=models.BooleanField(default=True),
        ),
    ]
