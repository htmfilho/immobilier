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
import factory
import factory.fuzzy
import operator
from main.tests.factories.localite import LocaliteFactory
from django.conf import settings
from django.utils import timezone
from faker import Faker
fake = Faker()


def _get_tzinfo():
    if settings.USE_TZ:
        return timezone.get_current_timezone()
    else:
        return None


class BatimentFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'main.Batiment'

    rue = factory.Sequence(lambda n: 'Rue - %d' % n)
    numero = factory.fuzzy.FuzzyInteger(1, 100)
    boite = factory.Sequence(lambda n: '%d' % n)
    lieu_dit = factory.Sequence(lambda n: 'Lieu dit - %d' % n)
    #localite = models.ForeignKey('Localite')
    localite = factory.SubFactory(LocaliteFactory)

    # superficie = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    # performance_energetique = models.CharField(max_length=30, blank=True, null=True)