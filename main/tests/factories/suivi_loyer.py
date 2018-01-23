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
from main.tests.factories.financement_location import FinancementLocationFactory
from main.models.enums import etat_suivi
import operator


fake = Faker()


def _get_tzinfo():
    if settings.USE_TZ:
        return timezone.get_current_timezone()
    else:
        return None


class SuiviLoyerFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'main.SuiviLoyer'

    financement_location = factory.SubFactory(FinancementLocationFactory)

    date_paiement = factory.Faker('date_time_this_decade', before_now=True, after_now=False, tzinfo=_get_tzinfo())
    etat_suivi = factory.Iterator(etat_suivi, getter=operator.itemgetter(0))
    # remarque = models.TextField(blank=True, null=True)
    # loyer_percu = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    # charges_percu = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    # date_paiement_reel = models.DateField(blank=True, null=True)

