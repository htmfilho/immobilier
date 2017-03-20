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
from main.models import professionnel as Professionnel
from main.models import personne as Personne
from main.models import proprietaire as Proprietaire

class Locataire(models.Model):
    CIVILITE = (
        ('NON_PRECISE', '-'),
        ('MADAME', 'Madame'),
        ('MADEMOISELLE', 'Mademoiselle'),
        ('MONSIEUR', 'Monsieur'),
        ('MAITRE', 'Maitre'),
        ('DOCTEUR', 'Docteur'),
    )
    personne = models.ForeignKey('Personne', error_messages={'unique': 'Please enter your name'})
    contrat_location = models.ForeignKey('ContratLocation', default=None)
    infos_complement = models.TextField(blank=True, null=True)
    principal = models.BooleanField(default=True)
    societe = models.ForeignKey('Societe', blank=True, null=True)
    tva = models.CharField(max_length=30, blank=True, null=True)
    profession = models.ForeignKey('Fonction', blank=True, null=True)
    civilite = models.CharField(max_length=15, choices=CIVILITE, default='NON_PRECISE')
    # personne_garante     = models.ForeignKey('Personne', blank=True, null=True)

    def __str__(self):
        return self.personne.nom + ", " + self.personne.prenom

    # def unique_error_message(self, model_class, unique_check):
    #     print('uni')
    #     if model_class == type(self) and unique_check == ('personne', 'contrat_location'):
    #         return "kkk"
    #     else:
    #         return super(Locataire, self).unique_error_message(model_class, unique_check)
    #
    class Meta:
        unique_together = (("personne", "contrat_location"),)

    def save(self,  *args, **kwargs):

        c = super(Locataire, self).save(*args, **kwargs)
        professionnels = Professionnel.search(self.personne, self.societe, self.profession)
        if not professionnels.exists():
            professionnel = Professionnel()
            professionnel.personne = self.personne
            professionnel.societe = self.societe
            professionnel.fonction = self.profession
            professionnel.save()
        return c


def find_my_locataires():
    personne = Personne.find_gestionnaire_default()
    l = []
    if personne:
        batiments = Proprietaire.find_batiment_by_personne(personne)
        for b in batiments:
            l.extend(b.locataires_actuels2())
    return l


def find_by_contrat_location(contrat):
    return Locataire.objects.filter(contrat_location=contrat)

def find_all():
    return Locataire.objects.all()