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
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from main import contratgestion
from main.tests.factories.batiment import BatimentFactory
from main.tests.factories.contrat_gestion import ContratGestionFactory
from main.models.enums import alerte_etat
from main import models as mdl
from main import pages_utils


class ContratGestionViewTest(TestCase):

    def setUp(self):
        self.batiment_1 = BatimentFactory()
        self.contrat_gestion_1 = ContratGestionFactory(batiment=self.batiment_1)

    def test_list(self):
        expected_objects = [self.contrat_gestion_1]

        url = reverse('contratgestion_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, contratgestion.CONTRATGESTION_LIST_HTML)
        self.assertEqual(list(response.context['contrats']), expected_objects)

    def test_delete(self):
        un_batiment = BatimentFactory()
        contrat_gestion_a_supprimer = ContratGestionFactory(batiment=un_batiment)
        url = reverse('contratgestion-delete', args=[contrat_gestion_a_supprimer.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, pages_utils.PAGE_BATIMENT_FORM)
        self.assertEqual(response.context['batiment'], un_batiment)
