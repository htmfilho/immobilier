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
from django.test import TestCase
from django.core.urlresolvers import reverse
from main import contratlocation
from main.tests.factories.contrat_location import ContratLocationFactory
from django.utils import timezone
import datetime



date_debut =  datetime.datetime(timezone.now().year-1, 1, 1)
date_fin = datetime.datetime(timezone.now().year + 1, 1, 1)


class ContratLocationViewTest(TestCase):

    def setUp(self):
        self.contrat_location_1 = ContratLocationFactory(date_debut=date_debut,
                                                         date_fin=date_fin)
        self.contrat_location_1.date_fin=date_fin
        self.contrat_location_1.date_debut=date_debut

    # Problème dans le test ci-dessous?????
    # def test_list(self):
    #     print(self.contrat_location_1)
    #     expected_objects = [self.contrat_location_1]
    #
    #     url = reverse('contratlocation_list')
    #     response = self.client.get(url)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, contratlocation.CONTRAT_LOCATION_LIST_HTML)
    #     self.assertEqual(response.context['locations'].count(), 1)

    def test_delete(self):
        contrat_location_a_supprimer = ContratLocationFactory(date_debut=date_debut,
                                                              date_fin=date_fin)
        url = reverse('location-delete', args=[contrat_location_a_supprimer.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
