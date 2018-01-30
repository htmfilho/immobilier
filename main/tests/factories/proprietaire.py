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
from main.tests.factories.personne import PersonneFactory
from main.tests.factories.batiment import BatimentFactory


class ProprietaireFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'main.Proprietaire'

    proprietaire = factory.SubFactory(PersonneFactory)
    batiment = factory.SubFactory(BatimentFactory)
    date_debut = None
    date_fin = None
    # actif = models.BooleanField(default=True)

