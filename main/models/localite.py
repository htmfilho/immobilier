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


class Localite(models.Model):
    code_postal = models.CharField(max_length=10, blank=False, null=False)
    localite = models.CharField(max_length=150, blank=False, null=False)
    pays = models.ForeignKey('Pays', blank=True, null=True)

    def __str__(self):
        return self.code_postal + " " + self.localite

    class Meta:
        ordering = ['localite']


def autocomplete_search_fields():
    return 'localite', 'code_postal'


def find_all():
    return Localite.objects.all()


def find_by_id(an_id):
    return Localite.objects.get(pk=an_id)


def search(un_code_postal, une_localite):
    out = None
    queryset = Localite.objects
    if un_code_postal:
        queryset = queryset.filter(code_postal=un_code_postal)

    if une_localite:
        queryset = queryset.filter(localite__iexact=une_localite)

    if un_code_postal or une_localite:
        out = queryset
    return out

def create_localite(nom, cp):
    localite = mdl.localite.Localite()
    localite.localite = nom
    localite.code_postal = cp
    localite.save()
    return localite
