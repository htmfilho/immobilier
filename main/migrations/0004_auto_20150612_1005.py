# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150611_1159'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contrat',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date_debut', models.DateField(auto_now=True)),
                ('date_fin', models.DateField(blank=True, null=True)),
                ('renonciation', models.DateField()),
                ('loyer_base', models.DecimalField(max_digits=5, decimal_places=2, default=0)),
                ('charges_base', models.DecimalField(max_digits=5, decimal_places=2, default=0)),
                ('index_base', models.DecimalField(max_digits=5, decimal_places=2, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ContratGestion',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date_debut', models.DateField(auto_now=True)),
                ('date_fin', models.DateField(blank=True, null=True)),
                ('gestionnaire', models.ForeignKey(to='main.Personne')),
            ],
        ),
        migrations.CreateModel(
            name='FraisMaintenance',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('description', models.TextField()),
                ('montant', models.DecimalField(decimal_places=2, max_digits=5)),
                ('date_realisation', models.DateField()),
                ('entrepreneur', models.ForeignKey(to='main.Personne')),
            ],
        ),
        migrations.CreateModel(
            name='Proprietaire',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date_debut', models.DateField(blank=True, null=True)),
                ('date_fin', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SuiviLoyer',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date_paiement', models.DateField()),
                ('etat_suivi', models.CharField(max_length=10, default='A_VERIFIER', choices=[('A_VERIFIER', 'A vérifier'), ('IMPAYE', 'Impayé'), ('EN_RETARD', 'En retard'), ('PAYE', 'Payé')])),
                ('remarque', models.TextField(blank=True, null=True)),
                ('loyer_percu', models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=5)),
                ('charges_percu', models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.RenameField(
            model_name='locataire',
            old_name='infos_compl',
            new_name='infos_complement',
        ),
        migrations.AddField(
            model_name='batiment',
            name='peformance_energetique',
            field=models.CharField(blank=True, null=True, max_length=10),
        ),
        migrations.AddField(
            model_name='locataire',
            name='profession',
            field=models.CharField(blank=True, null=True, max_length=50),
        ),
        migrations.AddField(
            model_name='locataire',
            name='societe',
            field=models.CharField(blank=True, null=True, max_length=100),
        ),
        migrations.AddField(
            model_name='locataire',
            name='tva',
            field=models.CharField(blank=True, null=True, max_length=30),
        ),
        migrations.AddField(
            model_name='location',
            name='assurance',
            field=models.ForeignKey(null=True, to='main.Assurance', blank=True),
        ),
        migrations.AddField(
            model_name='location',
            name='charges',
            field=models.DecimalField(max_digits=5, decimal_places=2, default=0),
        ),
        migrations.AddField(
            model_name='location',
            name='index',
            field=models.DecimalField(max_digits=5, decimal_places=2, default=0),
        ),
        migrations.AddField(
            model_name='location',
            name='loyer',
            field=models.DecimalField(max_digits=5, decimal_places=2, default=0),
        ),
        migrations.AddField(
            model_name='suiviloyer',
            name='location',
            field=models.ForeignKey(to='main.Location'),
        ),
        migrations.AddField(
            model_name='proprietaire',
            name='batiment',
            field=models.ForeignKey(to='main.Batiment'),
        ),
        migrations.AddField(
            model_name='proprietaire',
            name='proprietaire',
            field=models.ForeignKey(to='main.Personne'),
        ),
        migrations.AddField(
            model_name='fraismaintenance',
            name='proprietaire',
            field=models.ForeignKey(to='main.Proprietaire'),
        ),
        migrations.AddField(
            model_name='contratgestion',
            name='proprietaire',
            field=models.ForeignKey(to='main.Proprietaire'),
        ),
        migrations.AddField(
            model_name='contrat',
            name='location',
            field=models.ForeignKey(to='main.Location'),
        ),
    ]
