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


class FinancementLocation(models.Model):
    contrat_location = models.ForeignKey('ContratLocation', default=None)
    date_debut = models.DateField(auto_now=False, auto_now_add=False, verbose_name=u"Date début")
    date_fin = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    loyer = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    charges = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    index = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        chaine = str(self.loyer) + "/" + str(self.charges)
        if self.date_debut:
            chaine = chaine + " (" + self.date_debut.strftime('%d-%m-%Y')
        if self.date_fin:
            chaine = chaine + " au " + self.date_fin.strftime('%d-%m-%Y') + ")"
        if chaine:
            return chaine
        return ""

def find_by_location(une_location):
    return FinancementLocation.objects.filter(contrat_location=une_location)

def create(date_debut, date_fin, loyer_base):
    return FinancementLocation(date_debut=date_debut, date_fin=date_fin, loyer=loyer_base)