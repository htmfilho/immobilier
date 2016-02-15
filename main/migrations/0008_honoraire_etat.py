# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20160215_0808'),
    ]

    operations = [
        migrations.AddField(
            model_name='honoraire',
            name='etat',
            field=models.CharField(max_length=10, choices=[('A_VERIFIER', 'A vérifier'), ('IMPAYE', 'Impayé'), ('EN_RETARD', 'En retard'), ('PAYE', 'Payé')], default='A_VERIFIER', verbose_name='Etat'),
        ),
    ]
