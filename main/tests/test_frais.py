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
from main.tests.factories.frais_maintenance import FraisMaintenanceFactory
from main.tests.factories.professionnel import ProfessionnelFactory
from main.tests.factories.batiment import BatimentFactory
from main.models.enums import alerte_etat
from main import models as mdl
from main import frais as frais_view
from main.tests.factories.personne import PersonneFactory
from django.test.client import Client
from django.contrib.auth.models import User


class FraisViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

    def test_list_default(self):
        un_frais = FraisMaintenanceFactory()
        expected_objects = [un_frais]

        url = reverse('fraismaintenance_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, frais_view.FRAIS_LIST_HTML)
        self.assertEqual(list(response.context['frais_list']), expected_objects)

    def test_prepare_pour_la_mise_a_jour(self):
        un_frais = FraisMaintenanceFactory()

        entrepreneurs_attendus = self.get_entrepreneurs()

        url = reverse('fraismaintenance-prepare-update', args=[un_frais.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, frais_view.PAGE_FRAIS_FORM)
        self.assertEqual(response.context['frais'], un_frais)
        self.assertEqual(response.context['entrepreneurs'].count(), len(entrepreneurs_attendus))


    def test_new(self):
        url = reverse('fraismaintenance-new')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, frais_view.PAGE_FRAIS_FORM)

    def test_create(self):
        un_batiment = BatimentFactory()
        url = reverse('fraismaintenance-create', args=[un_batiment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, frais_view.PAGE_FRAIS_FORM)

    def get_entrepreneurs(self):
        entrepreneurs = []
        cpt = 0
        while cpt < 2:
            personne_1 = PersonneFactory(profession=None, fonction=None)
            entrepreneur_1 = ProfessionnelFactory(personne=personne_1)
            entrepreneurs.append(entrepreneur_1)
            cpt = cpt + 1

        return entrepreneurs

