# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20160122_1318'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pays',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('pays', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='alerte',
            name='contratGestion',
            field=models.ForeignKey(to='main.ContratGestion', verbose_name='Contrat de gestion', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='alerte',
            name='contratLocation',
            field=models.ForeignKey(to='main.ContratLocation', verbose_name='Contrat location', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='alerte',
            name='date_alerte',
            field=models.DateField(blank=True, null=True, verbose_name='Date alerte'),
        ),
        migrations.AlterField(
            model_name='alerte',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='alerte',
            name='etat',
            field=models.CharField(verbose_name='Etat', max_length=10, choices=[('A_VERIFIER', 'A vérifier'), ('VERIFIER', 'Vérifier'), ('COURRIER', 'Courrier à préparer')], default='A_VERIFIER'),
        ),
    ]
