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


class ProfessionnelAdmin(admin.ModelAdmin):
    search_fields = ['societe', 'personne']
    list_display = ('personne', 'societe', 'fonction')
    list_filter = ('societe', 'fonction')


class Professionnel(models.Model):
    personne = models.ForeignKey('Personne', blank=True, null=True)
    societe = models.ForeignKey('Societe', blank=True, null=True)
    fonction = models.ForeignKey('Fonction', blank=True, null=True)
    actif = models.BooleanField(default=False)

    @staticmethod
    def find_all():
        return Professionnel.objects.all().order_by('societe')

    def __str__(self):
        ch = ""
        if self.societe:
            ch = ch + " " + str(self.societe)
        else:
            ch = ch + " "

        if self.personne:
            ch = ch + "-" + str(self.personne)
        else:
            ch = " "

        if self.fonction:
            ch = ch + "-" + str(self.fonction)
        else:
            ch = ch + " "
        return ch


def search(personne=None, societe=None, fonction=None):
    out = None
    queryset = Professionnel.objects
    if personne:
        queryset = queryset.filter(personne=personne)
    if societe:
        queryset = queryset.filter(societe=societe)
    if fonction:
        queryset = queryset.filter(fonction=fonction)
    if personne or societe or fonction:
        out = queryset
    return out


def create():
    return Professionnel()


def find_by_societe(une_societe):
    return search(None, une_societe, None)


def find_all():
    return Professionnel.objects.all()


def find_by_personne(une_personne):
    return Professionnel.objects.filter(personne=une_personne)
