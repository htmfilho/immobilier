# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-30 06:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_modeledocument_modele'),
    ]

    operations = [
        migrations.AddField(
            model_name='personne',
            name='titre',
            field=models.CharField(blank=True, choices=[('NON_PRECISE', 'Madame, Monsieur,'), ('MONSIEUR', 'Monsieur'), ('MADAME', 'Madame'), ('MADEMOISELLE', 'Mademoiselle'), ('MAITRE', 'Maître')], default='NON_PRECISE', max_length=20, null=True),
        ),
    ]
