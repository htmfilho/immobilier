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
from main.models import batiment as Batiment
from django.utils import timezone
from django.contrib import admin


class FraisMaintenanceAdmin(admin.ModelAdmin):
    search_fields = ['batiment']
    list_display = ('batiment', 'description', 'montant')


class FraisMaintenance(models.Model):
    batiment = models.ForeignKey('Batiment', verbose_name=u"Batiment", blank=True, null=True)
    contrat_location = models.ForeignKey('ContratLocation', blank=True, null=True)
    entrepreneur = models.ForeignKey('Professionnel', blank=True, null=True)
    societe = models.ForeignKey('Societe', blank=True, null=True)
    description = models.TextField()
    montant = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    date_realisation = models.DateField(auto_now=False,
                                        auto_now_add=False,
                                        blank=True,
                                        null=True,
                                        verbose_name=u"Date réalisation")

    def __str__(self):
        ch = ""

        if self.description:
            ch = ch + "" + self.description
        return ch


def find_by_batiment(a_batiment):
    if a_batiment:
        return FraisMaintenance.objects.filter(batiment=a_batiment)
    return None


def find_mes_frais_du_mois():
    batiments = Batiment.find_batiments_gestionnaire()
    frais = []
    maintenant = timezone.now()
    if batiments:
        for batiment in batiments:
            recuperer_frais_hors_location(batiment, frais, maintenant)
    return frais


def recuperer_frais_hors_location(b, frais_param, n):
    frais = frais_param
    frais_liste = find_by_batiment(b)
    for f in frais_liste:
        if f.contrat_location is None and f.date_realisation is not None \
                and (f.date_realisation.month == n.month and f.date_realisation.year == n.year) and f not in frais:
            frais.append(f)
    return frais


def find_by_id(id):
    return FraisMaintenance.objects.get(pk=id)


def find_all():
    return FraisMaintenance.objects.all()


def find_by_contrat_location(contrat_location_id):
    return FraisMaintenance.objects.filter(contrat_location=contrat_location_id)
