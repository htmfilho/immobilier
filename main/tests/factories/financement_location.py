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
import factory
import factory.fuzzy
import string
from django.conf import settings
from django.utils import timezone
from faker import Faker
from main.tests.factories.contrat_location import ContratLocationFactory

def generate_date_debut(financement_location):
    return financement_location.date_debut

def generate_date_fin(financement_location):
    return financement_location.date_fin

class FinancementLocationFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'main.FinancementLocation'

    contrat_location = factory.SubFactory(ContratLocationFactory)
    date_debut = generate_date_debut
    date_fin = generate_date_fin
    loyer = factory.fuzzy.FuzzyDecimal(250.50, 480.0)
    charges = factory.fuzzy.FuzzyDecimal(250.50, 480.0)
    # index = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    # indice_sante = models.ForeignKey('IndiceSante', default=None, blank=True, null=True)