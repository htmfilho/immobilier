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
from main.models.enums import alerte_etat
from django.conf import settings
from django.utils import timezone
from faker import Faker


fake = Faker()


def _get_tzinfo():
    if settings.USE_TZ:
        return timezone.get_current_timezone()
    else:
        return None


class AlerteFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'main.Alerte'

    description = factory.Sequence(lambda n: 'Description - %d' % n)
    date_alerte = fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=_get_tzinfo())

    # contrat_gestion = models.ForeignKey('ContratGestion', blank=True, null=True, verbose_name=u"Contrat de gestion")
    # contrat_location = models.ForeignKey('ContratLocation', blank=True, null=True, verbose_name=u"Contrat location")
    etat = factory.Iterator(alerte_etat.ETATS, getter=operator.itemgetter(0))


