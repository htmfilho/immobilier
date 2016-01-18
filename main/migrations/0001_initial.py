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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Banque',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Batiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('rue', models.CharField(max_length=200, blank=True, null=True)),
                ('numero', models.IntegerField(blank=True, null=True)),
                ('boite', models.CharField(max_length=10, blank=True, null=True)),
                ('lieu_dit', models.CharField(max_length=200, blank=True, null=True)),
                ('code_postal', models.CharField(max_length=10, blank=True, null=True)),
                ('localite', models.CharField(max_length=150, blank=True, null=True)),
                ('superficie', models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)),
                ('peformance_energetique', models.CharField(max_length=10, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContratGestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date_debut', models.DateField(auto_now=True)),
                ('date_fin', models.DateField(blank=True, null=True)),
                ('batiment', models.ForeignKey(to='main.Batiment')),
            ],
        ),
        migrations.CreateModel(
            name='ContratLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField(blank=True, null=True)),
                ('renonciation', models.DateField(blank=True, null=True)),
                ('remarque', models.TextField(blank=True, null=True)),
                ('assurance', models.ForeignKey(to='main.Assurance', blank=True, null=True)),
                ('batiment', models.ForeignKey(to='main.Batiment')),
            ],
        ),
        migrations.CreateModel(
            name='FinancementLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField(blank=True, null=True)),
                ('loyer', models.DecimalField(max_digits=6, decimal_places=2, default=0)),
                ('charges', models.DecimalField(max_digits=6, decimal_places=2, default=0)),
                ('index', models.DecimalField(max_digits=5, decimal_places=2, default=0)),
                ('contrat_location', models.ForeignKey(default=None, to='main.ContratLocation')),
            ],
        ),
        migrations.CreateModel(
            name='FraisMaintenance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('description', models.TextField()),
                ('montant', models.DecimalField(max_digits=8, decimal_places=2, default=0)),
                ('date_realisation', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Locataire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('infos_complement', models.TextField(blank=True, null=True)),
                ('principal', models.BooleanField(default=True)),
                ('societe', models.CharField(max_length=100, blank=True, null=True)),
                ('tva', models.CharField(max_length=30, blank=True, null=True)),
                ('profession', models.CharField(max_length=50, blank=True, null=True)),
                ('contrat_location', models.ForeignKey(default=None, to='main.ContratLocation')),
            ],
        ),
        migrations.CreateModel(
            name='ModeleDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('type_document', models.CharField(max_length=50)),
                ('contenu', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('societe', models.CharField(max_length=100, blank=True, null=True)),
                ('email', models.EmailField(max_length=254, blank=True, null=True)),
                ('profession', models.CharField(max_length=100, blank=True, null=True)),
                ('date_naissance', models.DateField(blank=True, null=True)),
                ('lieu_naissance', models.CharField(max_length=100, blank=True, null=True)),
                ('pays_naissance', models.CharField(max_length=100, blank=True, null=True)),
                ('num_identite', models.CharField(max_length=100, blank=True, null=True)),
                ('telephome', models.CharField(max_length=30, blank=True, null=True)),
                ('gsm', models.CharField(max_length=30, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proprietaire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date_debut', models.DateField(blank=True, null=True)),
                ('date_fin', models.DateField(blank=True, null=True)),
                ('batiment', models.ForeignKey(to='main.Batiment')),
                ('proprietaire', models.ForeignKey(to='main.Personne')),
            ],
        ),
        migrations.CreateModel(
            name='SuiviLoyer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date_paiement', models.DateField()),
                ('etat_suivi', models.CharField(max_length=10, choices=[('A_VERIFIER', 'A vérifier'), ('IMPAYE', 'Impayé'), ('EN_RETARD', 'En retard'), ('PAYE', 'Payé')], default='A_VERIFIER')),
                ('remarque', models.TextField(blank=True, null=True)),
                ('loyer_percu', models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)),
                ('charges_percu', models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)),
                ('financement_location', models.ForeignKey(to='main.FinancementLocation')),
            ],
        ),
        migrations.AddField(
            model_name='locataire',
            name='personne',
            field=models.ForeignKey(to='main.Personne'),
        ),
        migrations.AddField(
            model_name='fraismaintenance',
            name='entrepreneur',
            field=models.ForeignKey(to='main.Personne', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fraismaintenance',
            name='proprietaire',
            field=models.ForeignKey(to='main.Proprietaire'),
        ),
        migrations.AddField(
            model_name='contratgestion',
            name='gestionnaire',
            field=models.ForeignKey(to='main.Personne'),
        ),
    ]
