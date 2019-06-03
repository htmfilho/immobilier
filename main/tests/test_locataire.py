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
from django.test import TestCase
from django.core.urlresolvers import reverse
from main.tests.factories.personne import PersonneFactory
from main.tests.factories.societe import SocieteFactory
from main.tests.factories.localite import LocaliteFactory
from main.tests.factories.contrat_location import ContratLocationFactory
from main.tests.factories.locataire import LocataireFactory
from main.tests.factories.type_societe import TypeSocieteFactory
from django.test.client import Client
from django.contrib.auth.models import User
from main.tests.factories.fonction import FonctionFactory
from main.locataire import get_common_data
from main.pages_utils import LOCATAIRE_FORM_HTML
from main.forms.locataire import LocataireForm
from main.forms.personne_form import PersonneSimplifieForm
from main.models.personne import search as search_personne
from django.contrib.messages import get_messages


class LocataireViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

        self.personne_location1 = PersonneFactory(nom="Dupuis", prenom="Marcel")
        self.location_1 = ContratLocationFactory()
        self.locataire_1 = LocataireFactory(personne=self.personne_location1,
                                            contrat_location=self.location_1)
        self.url_add_nouveau_locataire = url = reverse("locataire-add")


    def test_form(self):
        url = reverse("locataire", args=[self.locataire_1.id])

        response = self.client.get(url)

        self.assertTemplateUsed(response, LOCATAIRE_FORM_HTML)
        self.assertIsInstance(response.context['form'], LocataireForm)

    def test_new(self):
        url = reverse("locataire-new", args=[self.location_1.id])

        response = self.client.get(url)

        self.assertTemplateUsed(response, LOCATAIRE_FORM_HTML)
        self.assertIsInstance(response.context['form'], LocataireForm)
        self.assertIsInstance(response.context['form_personne_simplifiee'], PersonneSimplifieForm)

    def test_add_invalid(self):
        response = self.client.post(self.url_add_nouveau_locataire, data={'location_id': self.location_1.id})
        self.assertEqual(response.status_code, 200)

class LocataireTest(TestCase):

    def test_get_common_data(self):
        fonction = FonctionFactory()
        personne = PersonneFactory(fonction=fonction,
                                   profession=fonction.nom_fonction)
        type_societe = TypeSocieteFactory()
        localite = LocaliteFactory()
        societe = SocieteFactory(localite=localite)

        data = get_common_data()
        self.assertCountEqual(data['type_societes'], [type_societe])
        self.assertCountEqual(data['personnes'], [personne])
        self.assertCountEqual(data['localites'], [localite])
        self.assertCountEqual(data['fonctions'], [fonction])
        self.assertCountEqual(data['societes'], [societe])
