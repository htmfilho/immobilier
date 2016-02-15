# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_honoraire_etat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='honoraire',
            name='contrat_gestion',
            field=models.ForeignKey(verbose_name='Contrat de gestion', to='main.ContratGestion', blank=True, null=True),
        ),
    ]
