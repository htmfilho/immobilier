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
from main.models import contrat_gestion as ContratGestion


class HonoraireAdmin(admin.ModelAdmin):
    list_filter = ('etat',)


class Honoraire(models.Model):
    ETAT_HONORAIRE = (
        ('A_VERIFIER', 'A vérifier'),
        ('IMPAYE', 'Impayé'),
        ('EN_RETARD', 'En retard'),
        ('PAYE', 'Payé')
    )
    contrat_gestion = models.ForeignKey('ContratGestion', blank=True, null=True, verbose_name=u"Contrat de gestion")
    date_paiement = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,
                                     verbose_name=u"Date paiement")
    etat = models.CharField(max_length=10, choices=ETAT_HONORAIRE, default='A_VERIFIER', verbose_name=u"Etat")

    def __str__(self):
        if self.contrat_gestion:
            return str(self.contrat_gestion)
        else:
            return ""


def find_honoraires_by_etat_today(etat):
    date_d = timezone.now() - relativedelta(months=1)
    date_f = timezone.now() + relativedelta(months=1)
    return Honoraire.objects.filter(etat=etat, date_paiement__lte=date_f, date_paiement__gte=date_d)


def find_all():
    return Honoraire.objects.all()


def find_by_batiment_etat_date(batiment_id, etat, date_limite_inf, date_limite_sup):
    queryset = Honoraire.objects

    if batiment_id:
        queryset = queryset.filter(contrat_gestion__batiment__id=int(batiment_id))

    if etat is not None and len(etat) > 0:
        queryset = queryset.filter(etat=etat)

    if date_limite_inf:
        queryset = queryset.filter(date_paiement__gte=date_limite_inf)

    if date_limite_sup:
        queryset = queryset.filter(date_paiement__lte=date_limite_sup)

    return queryset


def find_all_batiments():
    batiments = []
    for c in ContratGestion.find_all():
        if c.batiment not in batiments:
            batiments.append(c.batiment)
    return batiments
