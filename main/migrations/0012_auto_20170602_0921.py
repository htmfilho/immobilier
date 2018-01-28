# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-02 07:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20170530_1012'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pays',
            old_name='pays',
            new_name='nom',
        ),
        migrations.AlterField(
            model_name='personne',
            name='pays_naissance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Pays'),
        ),
    ]
