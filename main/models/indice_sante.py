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
import datetime
from django.db import models
from django.contrib import admin


class IndiceSanteAdmin(admin.ModelAdmin):
    list_filter = ('annee_base','date_calcul')


class IndiceSante(models.Model):
    date_calcul = models.DateField(auto_now=False, auto_now_add=False)
    annee_base = models.IntegerField()
    indice = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=False, null=False)

    class Meta:
        unique_together = ('date_calcul', 'annee_base',)


    def __str__(self):
        ch = ""
        if self.date_calcul:
            ch += str(self.date_calcul)
        else:
            ch += ' - '
        if self.annee_base:
            ch = "{} {}".format(ch, str(self.annee_base))
        else:
            ch = '{} - '.format(ch)
        if self.indice:
            ch = "{} {}".format(ch, str(self.indice))
        else:
            ch = '{} - '.format(ch)
        return ch


def find_by_date(date_ref):
    date_reference = datetime.datetime( date_ref.year, date_ref.month , 1 )
    return IndiceSante.objects.filter(date_calcul=date_reference).first()
