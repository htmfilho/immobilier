# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-20 14:08
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20170307_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='modeledocument',
            name='sujet',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='modeledocument',
            name='contenu',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='modeledocument',
            name='type_document',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
