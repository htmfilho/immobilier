# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150611_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locataire',
            name='infos_compl',
            field=models.TextField(null=True, blank=True),
        ),
    ]
