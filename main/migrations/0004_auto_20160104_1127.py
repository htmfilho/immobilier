# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20160104_0849'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proprietaire',
            old_name='personne_proprietaire',
            new_name='proprietaire',
        ),
    ]
