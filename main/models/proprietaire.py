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
from main.models import batiment as Batiment


class Proprietaire(models.Model):
    proprietaire = models.ForeignKey('Personne', verbose_name=u"Propriétaire")
    batiment = models.ForeignKey('Batiment')
    date_debut = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, verbose_name=u"Date début")
    date_fin = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)

    @property
    def batiments(self):
        return Batiment.objects.filter(proprietaire=self)


    def __str__(self):
        ch = ""
        ch = ch + self.proprietaire.nom
        ch = ch + self.proprietaire.prenom
        ch = ch + self.batiment.rue
        ch = ch + self.batiment.localite.localite
        return ch

    def get_absolute_url(self):
        return reverse('proprietaire_list')

    class Meta:
        unique_together = (("proprietaire", "batiment"),)


def find_proprietaire(id):
    return Proprietaire.objects.get(pk=id)


def find_batiment_by_personne(personne):
    list_p = Proprietaire.objects.filter(proprietaire=personne)
    batiments = []
    for p in list_p:
        if p.batiment:
            batiments.append(p.batiment)
    return batiments


def find_all():
    return Proprietaire.objects.all().order_by('proprietaire')


def find_distinct_proprietaires():
    results = Proprietaire.objects.all().order_by('proprietaire')
    liste = []
    liste_personne = []
    for result in results:
        if result.proprietaire not in liste_personne:
            liste.append(result)
            liste_personne.append(result.proprietaire)
    return liste


def find_by_batiment(a_batiment):
    return Proprietaire.objects.filter(batiment=a_batiment)


def find_by_personne(personne):
    return Proprietaire.objects.filter(proprietaire=personne)


def search(une_personne=None, un_batiment=None):
    queryset = Proprietaire.objects

    if une_personne:
        queryset = queryset.filter(proprietaire=une_personne)

    if un_batiment:
        queryset = queryset.filter(batiment=un_batiment)
    return queryset