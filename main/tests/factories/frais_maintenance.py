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
import operator
from main.tests.factories.batiment import BatimentFactory
from main.tests.factories.contrat_location import ContratLocationFactory
from django.conf import settings
from django.utils import timezone
from django.conf import settings
from faker import Faker
fake = Faker()


def _get_tzinfo():
    if settings.USE_TZ:
        return timezone.get_current_timezone()
    else:
        return None


class FraisMaintenanceFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'main.FraisMaintenance'

    batiment = factory.SubFactory(BatimentFactory)
    contrat_location = factory.SubFactory(ContratLocationFactory)


    # entrepreneur = models.ForeignKey('Professionnel', blank=True, null=True)
    # societe = models.ForeignKey('Societe', blank=True, null=True)
    description = factory.Sequence(lambda n: 'Description - %d' % n)
    montant = factory.fuzzy.FuzzyDecimal(1, 480.0)
    date_realisation = factory.Faker('date_time_this_decade', before_now=True, after_now=False, tzinfo=_get_tzinfo())
