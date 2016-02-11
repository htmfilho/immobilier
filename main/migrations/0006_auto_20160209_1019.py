# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20160204_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locataire',
            name='personne',
            field=models.ForeignKey(to='main.Personne', error_messages={'unique': 'Please enter your name'}),
        ),
    ]
