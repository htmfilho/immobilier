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
from main.models import personne as Personne
from dateutil.relativedelta import relativedelta
from main import models as mdl
from django.core.validators import MinValueValidator


class ContratGestion(models.Model):
    batiment = models.ForeignKey('Batiment')
    gestionnaire = models.ForeignKey('Personne')
    date_debut = models.DateField(auto_now=False,  auto_now_add=False, blank=True, null=True)
    date_fin = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    montant_mensuel = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True,
                                          validators = [MinValueValidator(0)])


    def __str__(self):
        return self.gestionnaire.nom + ", " + self.gestionnaire.prenom + str(self.batiment)

    def save(self,  *args, **kwargs):

        c = super(ContratGestion, self).save(*args, **kwargs)

        if self.date_fin:
            alert = mdl.alerte.Alerte(description='Attention fin contrat location dans 4 mois',
                           date_alerte=self.date_fin - relativedelta(months=4), etat='A_VERIFIER', contrat_gestion=self)
            alert.save()
        if self.date_debut and self.date_fin:
            date_d = self.date_debut
            date_f = self.date_debut + relativedelta(months=1)
            i = 0
            while date_f <= self.date_fin:
                honoraire = mdl.honoraire.Honoraire(etat='A_VERIFIER', contrat_gestion=self, date_paiement=date_d)
                honoraire.save()
                date_d = date_d + relativedelta(months=1)
                date_f = date_f + relativedelta(months=1)
                i = i + 1

        return c


def find_by_id(id):
    return ContratGestion.objects.get(pk=id)


def find_all():
    return ContratGestion.objects.all()


def find_my_contrats():
    personne = Personne.find_gestionnaire_default()
    return ContratGestion.objects.filter(gestionnaire=personne)


def search(batiment, date_debut, date_fin):
    out = None
    queryset = ContratGestion.objects
    if batiment:
        queryset = queryset.filter(batiment=batiment)
    if date_debut:
        queryset = queryset.filter(date_debut_lte=date_debut)
    if date_fin:
        queryset = queryset.filter(date_fin_gte=date_fin)
    if batiment or date_debut or date_fin:
        out = queryset
    return out


def find_by_batiment(a_batiment):
    return ContratGestion.objects.filter(batiment=a_batiment)
