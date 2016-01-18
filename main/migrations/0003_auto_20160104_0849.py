# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150626_1349'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proprietaire',
            old_name='proprietaire',
            new_name='personne_proprietaire',
        ),
    ]
