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
from django.utils import timezone
from dateutil.relativedelta import relativedelta


class IndiceSanteAdmin(admin.ModelAdmin):
    list_filter = ('annee_base','date_calcul')


class IndiceSante(models.Model):

    date_calcul = models.DateField(auto_now=False, auto_now_add=False)
    annee_base = models.IntegerField()
    indice = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=False, null=False)

    def __str__(self):
        return self.date_calcul + " " + str(self.annee_base) + str(self.indice)



