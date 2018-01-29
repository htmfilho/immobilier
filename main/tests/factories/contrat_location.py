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
from main.tests.factories.batiment import BatimentFactory
from django.conf import settings
from django.utils import timezone
from django.conf import settings
from faker import Faker
fake = Faker()


def _get_tzinfo():
    if settings.USE_TZ:
        return timezone.get_current_timezone().date()
    else:
        return None


def generate_date_debut(contrat):
    return datetime.date(timezone.now().year, 1, 1)


def generate_date_fin(contrat):
    if contrat.date_debut:
        return datetime.date(timezone.now().year, 12, 31)
    else:
        return datetime.date(timezone.now().year+1, 9, 30)


class ContratLocationFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'main.ContratLocation'

    batiment = factory.SubFactory(BatimentFactory)

    # date_debut = factory.Faker('date_time_this_decade', before_now=True, after_now=False)
    date_debut = factory.LazyAttribute(generate_date_debut)
    date_fin = factory.LazyAttribute(generate_date_fin)
    # date_fin = factory.Faker('date_time_this_decade', before_now=False, after_now=True)
    # renonciation = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    # remarque = models.TextField(blank=True, null=True)
    # assurance = models.ForeignKey('Assurance', blank=True, null=True)
    loyer_base = factory.fuzzy.FuzzyDecimal(250.50, 480.0)
    charges_base = factory.fuzzy.FuzzyDecimal(250.50, 480.0)
    # indice_sante_base = models.ForeignKey('IndiceSante', default=None, blank=True, null=True)
