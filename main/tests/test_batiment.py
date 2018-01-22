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
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from main.tests.factories.batiment import BatimentFactory
from main.tests.factories.proprietaire import ProprietaireFactory
from main import batiment
import factory
from main.tests.factories.personne import PersonneFactory
from django.test.client import Client
from django.contrib.auth.models import User
from unittest import mock


class BatimentViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.personne = PersonneFactory()

    def test_search_par_proprietaire_non_defini(self):
        self.creer_5_batiments_avec_proprio()
        url = reverse('batiment_search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, batiment.PAGE_LISTE_BATIMENTS)

    def creer_5_batiments_avec_proprio(self):
        cpt = 0
        while cpt < 5:
            un_batiment = BatimentFactory()
            un_proprio = ProprietaireFactory(batiment=un_batiment)
            cpt = cpt + 1

