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
from django.contrib import admin
from django.db import models
from django.db.models import Q
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import datetime
import calendar
from main.models import batiment as Batiment
from main.models.enums import etat_suivi


class SuiviLoyerAdmin(admin.ModelAdmin):
    list_display = ('loyer_percu', 'etat_suivi', 'financement_location')
    fieldsets = ((None, {'fields': ('loyer_percu', 'etat_suivi', 'financement_location')}),)
    search_fields = ['etat_suivi', 'financement_location__contrat_location']
    raw_id_fields = ('financement_location', )

class SuiviLoyer(models.Model):
    financement_location = models.ForeignKey('FinancementLocation')
    date_paiement = models.DateField(auto_now=False, auto_now_add=False)
    etat_suivi = models.CharField(max_length=10, choices=etat_suivi.ETATS, default=etat_suivi.A_VERIFIER)
    remarque = models.TextField(blank=True, null=True)
    loyer_percu = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    charges_percu = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date_paiement_reel = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['date_paiement']

    def __str__(self):
        desc = ""
        if self.date_paiement:
            desc += self.date_paiement.strftime('%d-%m-%Y')

        if self.remarque:
            desc += " , (" + self.remarque + ")"

        if self.etat_suivi:
            desc += " (" + self.etat_suivi + ")"
        return desc


def find_suivis(date_d_param, date_f_param, etat_param):
    etat = get_param(etat_param)
    date_d = get_param(date_d_param)
    date_f = get_param(date_f_param)

    queryset = SuiviLoyer.objects
    if etat:
        queryset = queryset.filter(etat_suivi=etat)
    if date_d:
        queryset = queryset.filter(date_paiement__gte=date_d)
    if date_f:
        queryset = queryset.filter(date_paiement__lte=date_f)
    if etat or date_d or date_f:
        return queryset
    else:
        return SuiviLoyer.objects.all


def get_param(etat_param):
    if etat_param != "":
        return etat_param
    return None


def find_suivis_a_verifier():
    return SuiviLoyer.objects.filter(Q(date_paiement__gte=timezone.now(),
                                       date_paiement__lte=timezone.now() + relativedelta(months=1),
                                       etat_suivi=etat_suivi.A_VERIFIER)
                                     | Q(date_paiement__lte=timezone.now(), etat_suivi=etat_suivi.A_VERIFIER))


def find_suivis_a_verifier_proche():
    return SuiviLoyer.objects.filter(Q(date_paiement__lte=timezone.now() + relativedelta(months=2),
                                       etat_suivi=etat_suivi.A_VERIFIER))


def find_suivis_by_etat_suivi(date_ref, etat_suivi):
    start_date = datetime.datetime(date_ref.year, date_ref.month, 1)
    end_date = datetime.datetime(date_ref.year, date_ref.month, calendar.mdays[date_ref.month])
    return SuiviLoyer.objects.filter(date_paiement__lte=end_date, date_paiement__gte=start_date,
                                     etat_suivi=etat_suivi)


def find_mes_suivis_by_etat_suivi(date_ref, etat_suivi):
    mes_batiment = Batiment.find_batiments_gestionnaire()
    start_date = datetime.datetime(date_ref.year, date_ref.month, 1)
    end_date = datetime.datetime(date_ref.year, date_ref.month, calendar.mdays[date_ref.month])
    if mes_batiment:
        return SuiviLoyer.objects.filter(date_paiement__lte=end_date, date_paiement__gte=start_date,
                                         etat_suivi=etat_suivi,
                                         financement_location__contrat_location__batiment__in=mes_batiment)
    return None


def find_suivis_by_pas_etat_suivi(date_ref, etat_suivi):
    start_date = datetime.datetime(date_ref.year, date_ref.month, 1)
    end_date = datetime.datetime(date_ref.year, date_ref.month, calendar.mdays[date_ref.month])
    return SuiviLoyer.objects.filter(date_paiement__lte=end_date, date_paiement__gte=start_date)\
        .exclude(etat_suivi=etat_suivi)


def find_all():
    return SuiviLoyer.objects.all()


def find_suivis_paye(financement):
    # return SuiviLoyer.objects.filter(financement_location = financement, etat_suivi='PAYE')
    return SuiviLoyer.objects.all()


def find(financement_courant, date_debut, etat):
    return SuiviLoyer.objects.filter(financement_location=financement_courant,
                                     date_paiement__gte=date_debut,
                                     etat_suivi=etat)


def find_dernier_paye(un_contrat_location):
    resul = SuiviLoyer.objects.filter(financement_location__contrat_location=un_contrat_location,
                                      date_paiement_reel__isnull=False,
                                      etat_suivi='PAYE').order_by('-date_paiement_reel')

    return resul.first()
