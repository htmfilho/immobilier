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
from main.tests.factories.fonction import FonctionFactory
from main.tests.factories.pays import PaysFactory
from main.tests.factories.societe import SocieteFactory
from main.tests.factories.localite import LocaliteFactory
from main.tests.factories.contrat_location import ContratLocationFactory
from main.tests.factories.locataire import LocataireFactory
from main.tests.factories.type_societe import TypeSocieteFactory
from main import personne as personne_view
from django.test.client import Client
from django.contrib.auth.models import User
from main.tests.factories.fonction import FonctionFactory
from main.tests.factories.pays import PaysFactory
from main.locataire import get_personnes_non_locataires, get_common_data
from main.pages_utils import NEW, UPDATE, LOCATAIRE_FORM_HTML
from main.forms.locataire import LocataireForm
from main import models as mdl


class LocataireViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

        self.personne_location1 = PersonneFactory()
        self.location_1 = ContratLocationFactory()
        self.locataire_1 = LocataireFactory(personne=self.personne_location1,
                         contrat_location=self.location_1)

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


class LocataireTest(TestCase):

    def test_get_get_personnes_non_locataires(self):
        personne_1_location = PersonneFactory()
        personne_2_location = PersonneFactory()
        personne_location1 = PersonneFactory()

        location_1 = ContratLocationFactory()
        LocataireFactory(personne=personne_location1,
                         contrat_location=location_1)
        self.assertCountEqual(get_personnes_non_locataires(location_1),
                              [personne_1_location, personne_2_location])

        location_2 = ContratLocationFactory()
        LocataireFactory(contrat_location=location_2)


        self.assertCountEqual(get_personnes_non_locataires(location_2),
                              [personne_1_location, personne_2_location, personne_location1])

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
