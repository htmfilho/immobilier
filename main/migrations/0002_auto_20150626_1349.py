# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('photo', models.FileField(upload_to='photos')),
                ('texte', models.TextField(default='')),
            ],
        ),
        migrations.AddField(
            model_name='batiment',
            name='photo',
            field=models.ManyToManyField(blank=True, null=True, to='main.Photo'),
        ),
    ]
