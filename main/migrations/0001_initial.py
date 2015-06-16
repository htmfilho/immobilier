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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Banque',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Batiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('rue', models.CharField(blank=True, null=True, max_length=200)),
                ('numero', models.IntegerField(blank=True, null=True)),
                ('boite', models.CharField(blank=True, null=True, max_length=10)),
                ('lieu_dit', models.CharField(blank=True, null=True, max_length=200)),
                ('code_postal', models.CharField(blank=True, null=True, max_length=10)),
                ('localite', models.CharField(blank=True, null=True, max_length=150)),
                ('superficie', models.DecimalField(blank=True, max_digits=5, null=True, decimal_places=3)),
                ('peformance_energetique', models.CharField(blank=True, null=True, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ContratGestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_debut', models.DateField(auto_now=True)),
                ('date_fin', models.DateField(blank=True, null=True)),
                ('batiment', models.ForeignKey(to='main.Batiment')),
            ],
        ),
        migrations.CreateModel(
            name='ContratLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField(blank=True, null=True)),
                ('renonciation', models.DateField(blank=True, null=True)),
                ('remarque', models.TextField(blank=True, null=True)),
                ('assurance', models.ForeignKey(null=True, blank=True, to='main.Assurance')),
                ('batiment', models.ForeignKey(to='main.Batiment')),
            ],
        ),
        migrations.CreateModel(
            name='FinancementLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField(blank=True, null=True)),
                ('loyer', models.DecimalField(max_digits=6, decimal_places=2, default=0)),
                ('charges', models.DecimalField(max_digits=6, decimal_places=2, default=0)),
                ('index', models.DecimalField(max_digits=5, decimal_places=2, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FraisMaintenance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
                ('montant', models.DecimalField(max_digits=8, decimal_places=2, default=0)),
                ('date_realisation', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Locataire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('infos_complement', models.TextField(blank=True, null=True)),
                ('principal', models.BooleanField(default=True)),
                ('societe', models.CharField(blank=True, null=True, max_length=100)),
                ('tva', models.CharField(blank=True, null=True, max_length=30)),
                ('profession', models.CharField(blank=True, null=True, max_length=50)),
                ('financement_location', models.ForeignKey(to='main.FinancementLocation')),
            ],
        ),
        migrations.CreateModel(
            name='ModeleDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type_document', models.CharField(max_length=50)),
                ('contenu', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('societe', models.CharField(blank=True, null=True, max_length=100)),
                ('email', models.EmailField(blank=True, null=True, max_length=254)),
                ('profession', models.CharField(blank=True, null=True, max_length=100)),
                ('date_naissance', models.DateField(blank=True, null=True)),
                ('lieu_naissance', models.CharField(blank=True, null=True, max_length=100)),
                ('pays_naissance', models.CharField(blank=True, null=True, max_length=100)),
                ('num_identite', models.CharField(blank=True, null=True, max_length=100)),
                ('telephome', models.CharField(blank=True, null=True, max_length=30)),
                ('gsm', models.CharField(blank=True, null=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Proprietaire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_debut', models.DateField(blank=True, null=True)),
                ('date_fin', models.DateField(blank=True, null=True)),
                ('batiment', models.ForeignKey(to='main.Batiment')),
                ('proprietaire', models.ForeignKey(to='main.Personne')),
            ],
        ),
        migrations.CreateModel(
            name='SuiviLoyer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_paiement', models.DateField()),
                ('etat_suivi', models.CharField(choices=[('A_VERIFIER', 'A vérifier'), ('IMPAYE', 'Impayé'), ('EN_RETARD', 'En retard'), ('PAYE', 'Payé')], max_length=10, default='A_VERIFIER')),
                ('remarque', models.TextField(blank=True, null=True)),
                ('loyer_percu', models.DecimalField(blank=True, max_digits=5, null=True, decimal_places=2)),
                ('charges_percu', models.DecimalField(blank=True, max_digits=5, null=True, decimal_places=2)),
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
            field=models.ForeignKey(null=True, blank=True, to='main.Personne'),
        ),
        migrations.AddField(
            model_name='fraismaintenance',
            name='proprietaire',
            field=models.ForeignKey(to='main.Proprietaire'),
        ),
        migrations.AddField(
            model_name='contratlocation',
            name='financement_location',
            field=models.ForeignKey(to='main.FinancementLocation'),
        ),
        migrations.AddField(
            model_name='contratgestion',
            name='gestionnaire',
            field=models.ForeignKey(to='main.Personne'),
        ),
    ]
