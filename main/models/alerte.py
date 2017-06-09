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
from main.models.enums import alerte_etat



class AlerteAdmin(admin.ModelAdmin):
    list_filter = ('etat',)


class Alerte(models.Model):

    description = models.TextField(verbose_name=u"Description")
    date_alerte = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,
                                   verbose_name=u"Date alerte")
    contrat_gestion = models.ForeignKey('ContratGestion', blank=True, null=True, verbose_name=u"Contrat de gestion")
    contrat_location = models.ForeignKey('ContratLocation', blank=True, null=True, verbose_name=u"Contrat location")
    etat = models.CharField(max_length=10, choices=alerte_etat.ETATS, default=alerte_etat.A_VERIFIER, verbose_name=u"Etat")

    class Meta:
        ordering = ['date_alerte']


    def __str__(self):
        return self.date_alerte.strftime('%d-%m-%Y') + " " + self.etat


def find_by_id(id):
    return Alerte.objects.get(pk=id)


def find_by_etat(etat_alerte):
    return Alerte.objects.filter(etat=etat_alerte)


def find_by_etat_today(etat_alerte):
    date_d = timezone.now() - relativedelta(months=1)
    date_f = timezone.now() + relativedelta(months=1)
    return Alerte.objects.filter(etat=etat_alerte, date_alerte__lte=date_f, date_alerte__gte=date_d)