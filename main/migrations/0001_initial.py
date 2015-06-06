# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assurance',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Banque',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100, blank=True, null=True)),
                ('profession', models.CharField(max_length=100, blank=True, null=True)),
                ('date_naissance', models.DateField(blank=True, null=True)),
                ('lieu_naissance', models.CharField(max_length=100, blank=True, null=True)),
                ('pays_naissance', models.CharField(max_length=100, blank=True, null=True)),
                ('num_identite', models.CharField(max_length=100, blank=True, null=True)),
                ('telephome', models.CharField(max_length=30, blank=True, null=True)),
                ('gsm', models.CharField(max_length=30, blank=True, null=True)),
            ],
        ),
    ]
