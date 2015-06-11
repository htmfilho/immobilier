# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batiment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('description', models.TextField()),
                ('nom', models.CharField(blank=True, max_length=100, null=True)),
                ('localite', models.CharField(blank=True, max_length=150, null=True)),
                ('numero', models.IntegerField(blank=True, null=True)),
                ('boite', models.IntegerField(blank=True, null=True)),
                ('code_postal', models.CharField(blank=True, max_length=10, null=True)),
                ('ville', models.CharField(blank=True, max_length=100, null=True)),
                ('province', models.CharField(blank=True, max_length=100, null=True)),
                ('surface', models.DecimalField(blank=True, max_digits=5, decimal_places=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Locataire',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('infos_compl', models.TextField()),
                ('principal', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('date_debut', models.DateField(auto_now=True)),
                ('date_fin', models.DateField()),
                ('batiment', models.ForeignKey(to='main.Batiment')),
            ],
        ),
        migrations.AddField(
            model_name='locataire',
            name='location',
            field=models.ForeignKey(to='main.Location'),
        ),
        migrations.AddField(
            model_name='locataire',
            name='personne',
            field=models.ForeignKey(to='main.Personne'),
        ),
    ]
