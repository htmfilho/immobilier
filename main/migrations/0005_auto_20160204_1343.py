# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20160122_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='Localite',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('code_postal', models.CharField(max_length=10, null=True, blank=True)),
                ('localite', models.CharField(max_length=150, null=True, blank=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='locataire',
            unique_together=set([('personne', 'contrat_location')]),
        ),
    ]
