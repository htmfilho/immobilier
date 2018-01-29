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
from main import contratlocation as contratlocation_view
from main.tests.factories.contrat_location import ContratLocationFactory
from main.tests.factories.assurance import AssuranceFactory
from main.tests.factories.batiment import BatimentFactory
from django.utils import timezone
import datetime
from main import views_utils


date_debut = datetime.date(timezone.now().year, 1, 1)


class ContratLocationViewTest(TestCase):

    def setUp(self):
        self.contrat_location_1 = ContratLocationFactory(date_debut=date_debut)

    def test_list(self):
        url = reverse('contratlocation_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, contratlocation_view.CONTRAT_LOCATION_LIST_HTML)
        self.assertEqual(response.context['locations'].count(), 1)

    def test_delete(self):
        contrat_location_a_supprimer = ContratLocationFactory(date_debut=date_debut)
        url = reverse('location-delete', args=[contrat_location_a_supprimer.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_set_assurance_no_data(self):
        self.assertIsNone(contratlocation_view.get_assurance_location(views_utils.UNDEFINED))
        self.assertIsNone(contratlocation_view.get_assurance_location(None))

    def test_get_assurance_location(self):
        assurance_1 = AssuranceFactory()
        self.assertEqual(contratlocation_view.get_assurance_location(assurance_1.id), assurance_1)
        self.assertEqual(contratlocation_view.get_assurance_location(str(assurance_1.id)), assurance_1)

    def test_get_batiment_no_id(self):
        self.assertIsNone(contratlocation_view.get_batiment(None))

    def test_get_batiment(self):
        batiment_1 = BatimentFactory()
        self.assertEqual(contratlocation_view.get_batiment(batiment_1.id), batiment_1)
        self.assertEqual(contratlocation_view.get_batiment(str(batiment_1.id)), batiment_1)

    def test_is_prolongation(self):
        self.assertTrue(contratlocation_view.is_prolongation(contratlocation_view.ONE_YEAR_DURATION, True))
        self.assertTrue(contratlocation_view.is_prolongation(contratlocation_view.SEVEN_YEARS_DURATION, True))

    def test_is_not_prolongation(self):
        self.assertFalse(contratlocation_view.is_prolongation(contratlocation_view.ONE_YEAR_DURATION, False))
        self.assertFalse(contratlocation_view.is_prolongation(None, False))
        self.assertFalse(contratlocation_view.is_prolongation(None, True))

