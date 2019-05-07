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
import datetime
import factory
import factory.fuzzy
import string
from django.conf import settings
from django.utils import timezone
from faker import Faker
from main.tests.factories.fonction import FonctionFactory
from main.models.personne import NOM_GESTIONNAIRE, PRENOM_GESTIONNAIRE


def generate_personne_email(person):
    domain = factory.Faker('domain_name').generate({})
    return '{0.prenom}.{0.nom}@{1}'.format(person, domain).lower()


class PersonneFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'main.Personne'

    nom = factory.Faker('last_name')
    prenom = factory.Faker('first_name')
    prenom2 = factory.Faker('first_name')
    email = factory.LazyAttribute(generate_personne_email)
    profession = factory.Sequence(lambda n: 'Profession %d' % n)
    # date_naissance = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)
    # lieu_naissance = models.CharField(max_length=100, blank=True, null=True)
    # pays_naissance = models.ForeignKey('Pays', blank=True, null=True)
    # num_identite = models.CharField(max_length=100, blank=True, null=True, unique=False)
    # telephone = models.CharField(max_length=30, blank=True, null=True)
    # gsm = models.CharField(max_length=30, blank=True, null=True)
    # societe = models.ForeignKey('Societe', blank=True, null=True)
    # num_compte_banque = models.CharField(max_length=30, blank=True, null=True)
    # personne_type = models.CharField(max_length=20, choices=TYPE_PERSONNE, default='NON_PRECISE', blank=True, null=True)  # a enlever
    # fonction = models.ForeignKey('Fonction', blank=True, null=True)
    fonction = factory.SubFactory(FonctionFactory)


class GestionnairePersonneFactory(PersonneFactory):
    nom = NOM_GESTIONNAIRE
    prenom = PRENOM_GESTIONNAIRE
