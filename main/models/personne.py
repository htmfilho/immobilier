##############################################################################
#
#    Immobilier it's an application
#    designed to manage the core business of property management, buildings,
#    rental agreement and so on.
#
#    Copyright (C) 2016-2017 Verpoorten Leïla
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from django.db import models
from django.contrib import admin
from main.models import proprietaire as Proprietaire
from main.models import pays as Pays
from main.models import locataire as Locataire
from main.models import fonction as Fonction
from main.models import professionnel as Professionnel
from main.models import contrat_gestion as ContratGestion

PRENOM_GESTIONNAIRE = 'Stéphan'

NOM_GESTIONNAIRE = 'Marchal'


class PersonneAdmin(admin.ModelAdmin):
    search_fields = ['nom']
    list_filter = ('nom', 'prenom', 'prenom2')


class Personne(models.Model):

    # TYPE_PERSONNE = (
    #     ('NON_PRECISE', '-'),
    #     ('LOCATAIRE', 'Locataire'),
    #     ('PROFESSIONNEL', 'Professionnel'),
    #     ('PROPRIETAIRE', 'Propriétaire'),
    #     ('ANCIEN_LOCATAIRE', 'Ancien locataire'),
    #     ('ANCIEN_PROPRIETAIRE', 'Ancien propriétaire'),
    # )
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    prenom2 = models.CharField(max_length=100, blank=True, null=True)
    # societe        = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    date_naissance = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)
    lieu_naissance = models.CharField(max_length=100, blank=True, null=True)
    pays_naissance = models.ForeignKey('Pays', blank=True, null=True)
    num_identite = models.CharField(max_length=100, blank=True, null=True, unique=False)
    telephone = models.CharField(max_length=30, blank=True, null=True)
    gsm = models.CharField(max_length=30, blank=True, null=True)
    societe = models.ForeignKey('Societe', blank=True, null=True)
    num_compte_banque = models.CharField(max_length=30, blank=True, null=True)
    #personne_type = models.CharField(max_length=20, choices=TYPE_PERSONNE, default='NON_PRECISE', blank=True, null=True)  # a enlever
    fonction = models.ForeignKey('Fonction', blank=True, null=True)

    def __init__(self,  *args, **kwargs):
        super(Personne, self).__init__(*args, **kwargs)
        # self._meta.get_field_by_name('pays_naissance')[0]._choices = get_pays_choix()

    def __str__(self):
        return self.nom.upper() + ", " + self.prenom

    def choix(self):
        return []

    @property
    def batiments(self):
        proprietaire_list = Proprietaire.objects.filter(proprietaire=self)
        batiments = []
        for p in proprietaire_list:
            # batiments.append(p.batiments)
            for b in p.batiments:
                batiments.append(b)
        return batiments

    @property
    def type(self):
        type_personne = ""
        cpt = 0
        proprietaire_list = Proprietaire.find_by_personne(self)
        if proprietaire_list.exists():
            type_personne = "propriétaire"
            cpt = cpt + 1
        locataire_list = Locataire.find_by_personne(self)
        if locataire_list.exists():
            if cpt > 0:
                type_personne = type_personne + ", "
            type_personne = type_personne + "locataire"
            cpt = cpt + 1
        liste = Professionnel.find_by_personne(self)
        if liste.exists():
            if cpt > 0:
                type_personne = type_personne + ", "
            type_personne = type_personne + "professionnel"

        return type_personne

    def contrat_gestions(self):
        proprietaire_list = Proprietaire.find_by_personne(self)
        contrats = []
        for p in proprietaire_list:

            for b in p.batiments:
                contrat_gestion = ContratGestion.objects.filter(batiment=b)
                if contrat_gestion is not None:
                    contrats.append(contrat_gestion)
        return contrats

    class Meta:
        ordering = ['nom', 'prenom']
        unique_together = (("nom", "prenom", "prenom2"),)

    def save(self,  *args, **kwargs):
        p = super(Personne, self).save(*args, **kwargs)

        fonction = None
        if self.profession:
            fonction = Fonction.find_by_nom(self.profession)
            if fonction is None:
                fonction = Fonction.create()
                fonction.nom_fonction = self.profession
                fonction.save()
        if fonction:
            professionnels = Professionnel.search(self, self.societe, fonction)
            if not professionnels.exists():
                professionnel = Professionnel.create()
                professionnel.personne = self
                professionnel.societe = self.societe
                professionnel.fonction = fonction
                professionnel.save()
        self.fonction = fonction

        return p


def find_personne(id):
    try:
        return Personne.objects.get(pk=id)
    except:
        return None


def find_all():
    return Personne.objects.all()


def find_gestionnaire_default():
    list_personne = Personne.objects.filter(nom=NOM_GESTIONNAIRE,
                                            prenom=PRENOM_GESTIONNAIRE)
    if list_personne.exists():
        return list_personne.first()
    return None


def delete_personne(id):
    personne = find_personne(id)
    if personne:
        if personne != find_gestionnaire_default():
            personne.delete()
            return True
    return False


def find_personne_by_nom_prenom(un_nom, un_prenom, un_prenom2):
    return Personne.objects.filter(nom__iexact=un_nom, prenom__iexact=un_prenom, prenom2__iexact=un_prenom2)


def search(nom, prenom):

    query = find_all()

    if nom:
        query = query.filter(nom__icontains=nom)
    if prenom:
        query = query.filter(prenom__icontains=prenom)

    return query.order_by('nom', 'prenom')
