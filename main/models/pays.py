##############################################################################
#
#    Immobilier it's an application
#    designed to manage the core business of property management, buildings,
#    rental agreement and so on.
#
#    Copyright (C) 2016-2018 Verpoorten Leïla
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


class Pays(models.Model):
    nom = models.CharField(max_length=50)

    def __str__(self):
        return self.nom


def find_by_id(un_id):
    try:
        return Pays.objects.get(pk=un_id)
    except:
        return None


def find_by_pays(un_pays):
    return Pays.objects.filter(pays=un_pays)


def create(un_nom):
    p = Pays(nom=un_nom)
    return p


def find_all():
    return Pays.objects.all().order_by('nom')

