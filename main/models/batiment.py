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
from django.db.models import Sum
from django.contrib import admin
from main.exportUtils import export_xls_batiment
from main.pdfUtils import pdf_batiment
from main.models import personne as Personne
from main.models import proprietaire as Proprietaire
from main.models import contrat_location as ContratLocation
from main.models import locataire as Locataire
from main.models import frais_maintenance as FraisMaintenance
from main.models import suivi_loyer as SuiviLoyer
from main.models import contrat_gestion as ContratGestion
from itertools import chain


class BatimentAdmin(admin.ModelAdmin):
    search_fields = ['localite']
    actions = [export_xls_batiment, pdf_batiment]


class Batiment(models.Model):
    description = models.TextField(blank=True, null=True)
    rue = models.CharField(max_length=200, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    boite = models.CharField(max_length=10, blank=True, null=True)
    lieu_dit = models.CharField(max_length=200, blank=True, null=True)
    localite = models.ForeignKey('Localite')
    superficie = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    performance_energetique = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        ordering = ['localite', 'rue']

    def __str__(self):
        desc = ""
        cptr = 0
        if not(self.rue is None):
            desc += " " + self.rue
            cptr = cptr + 1
        if not(self.numero is None):
            if cptr > 0:
                desc += ", "
            desc += str(self.numero)
            cptr = cptr + 1
        if not(self.boite is None):
            if cptr > 0:
                desc += ", "
            desc += self.boite
            cptr = cptr + 1
        if self.localite is not None:
            if cptr > 0:
                desc += ", "
            desc += str(self.localite.localite)
        return desc

    def adresse_rue(self):
        adresse_complete = ""
        if self.rue is not None:
            adresse_complete += self.rue
        if self.numero is not None:
            adresse_complete += " " + str(self.numero)
        if self.boite is not None:
            adresse_complete += " " + str(self.boite)
        return adresse_complete

    def adresse_localite(self):
        adresse_complete = ""
        if self.localite is not None:
            adresse_complete += " " + str(self.localite.localite)
        return adresse_complete

    def proprietaires(self):
        return Proprietaire.find_by_batiment(self)

    def contrats_location(self):
        return ContratLocation.find_by_batiment(self)

    def contrats_location_next(self):
        return ContratLocation.find_by_batiment_date_debut_gte(self, self.location_actuelle.date_fin)

    def contrats_location_previous(self):
        return ContratLocation.find_by_batiment_date_fin_lte(self, self.location_actuelle.date_debut)

    def contrat_location_next(self):
        list_c = ContratLocation.find_by_batiment_date_debut_gte(self, date_debut__gte=self.location_actuelle.date_fin)
        if list_c:
            return list_c[0]
        return None

    def contrat_location_previous(self):
        list_c = ContratLocation.find_by_batiment_date_fin_lte(self, self.location_actuelle.date_debut)
        if list_c:
            return list_c[0]
        return None

    def locataires_actuels(self):
        liste = []
        contrats = ContratLocation.find_by_batiment_dates(self)
        if not(contrats is None):
            for contrat in contrats:
                locataire = Locataire.find_by_contrat_location(contrat)
                for l in locataire:
                    p = Personne.find_personne(l.personne.id)
                    liste.append(p)

        return liste

    def locataires_actuels2(self):
        liste = []

        contrats = ContratLocation.find_by_batiment_dates(self)
        if not(contrats is None):
            for contrat in contrats:
                locataire = Locataire.find_by_contrat_location(contrat)
                for l in locataire:
                    if l not in liste:
                        liste.append(l)

        return liste

    def dernier_locataires(self):
        liste = []
        contrats = ContratLocation.find_by_batiment(self)
        if contrats.exists():
            locataire = Locataire.find_by_contrat_location(contrats.last())
            for l in locataire:
                if l not in liste:
                    liste.append(l)

        return liste

    @property
    def location_actuelle(self):
        locations = ContratLocation.find_by_batiment_dates(self)
        if locations:
            return locations.first()
        else:
            return ContratLocation.find_last_by_batiment(self)

    def location_actuelle_pk(self):
        contrat_location = ContratLocation.find_by_batiment_dates(self)
        if contrat_location:
            return contrat_location.id
        return None

    @property
    def contrats_gestion(self):
        return ContratGestion.find_by_batiment(self)

    @property
    def frais_list(self):
        return FraisMaintenance.find_by_batiment(self)

    @property
    def gains(self):
        tot = 0
        for c in self.contrats_location():
            for f in c.financements():
                queryset = SuiviLoyer.find_suivis_paye(f)
                aggregation = queryset.aggregate(loyer=Sum('loyer_percu'))
                loyer = aggregation.get('loyer', 0)
                tot = tot + loyer

        return tot

    @property
    def depenses(self):
        queryset = FraisMaintenance.find_by_batiment(self)
        aggregation = queryset.aggregate(price=Sum('montant'))
        res = aggregation.get('price', 0)

        if res:
            return res

        return 0

    @property
    def location_en_cours(self):
        locations = ContratLocation.find_by_batiment_dates(self)
        if locations:
            return True
        return None

    @property
    def en_gestion(self):
        if ContratGestion.find_by_batiment(self).exists():
            return True
        return False



def autocomplete_search_fields():
    return 'localite'


def find_all():
    return Batiment.objects.all()


def find_batiment(id):
    return Batiment.objects.get(pk=id)


def find_batiments_gestionnaire():
    personne = Personne.find_gestionnaire_default()
    batiments_gestionnaire=[]
    if personne:
        batiments_gestionnaire =  Proprietaire.find_batiment_by_personne(personne)
        batiments_en_gestion = find_batiment_by_gestionnaire()
        # return batiments_gestionnaire
        # return chain(batiments_gestionnaire,batiments_en_gestion)
        # bats = []
        # for b in batiments_gestionnaire:
        #     bats.append(b)
        # for b in batiments_gestionnaire:
        #     bats.append(b)
        return  chain(batiments_gestionnaire, batiments_en_gestion)
    return None


def search_par_proprietaire(proprietaire_id=None):
    if proprietaire_id and proprietaire_id != "":
        proprio = Proprietaire.find_proprietaire(proprietaire_id)
        return Proprietaire.find_batiment_by_personne(proprio.proprietaire)
    return Batiment.objects.all()


def find_batiment_by_gestionnaire():
    res = []
    batiments_en_gestion = ContratGestion.find_my_contrats()
    for bat in batiments_en_gestion:
        if bat not in res:
            res.append(bat.batiment)
    return res


def find_by_proprietaire(a_proprietaire):
    return Batiment.objects.filter(proprietaire=a_proprietaire)