# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20160215_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personne',
            name='num_identite',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
