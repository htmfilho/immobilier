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
from main.tests.factories.batiment import BatimentFactory
from main.tests.factories.proprietaire import ProprietaireFactory
from main import batiment
import factory
from main.tests.factories.personne import PersonneFactory
from main.tests.factories.assurance import AssuranceFactory
from main.tests.factories.localite import LocaliteFactory
from django.test.client import Client
from django.contrib.auth.models import User
from unittest import mock
from main import pages_utils
from main import models as mdl


class BatimentViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.assurance_1 = AssuranceFactory()
        cls.assurance_2 = AssuranceFactory()

        cls.localite_1 = LocaliteFactory()
        cls.localite_2 = LocaliteFactory()

        creer_5_batiments_avec_proprio(cls.localite_1)

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.personne = PersonneFactory(fonction=None, societe=None)

    def test_search_par_proprietaire_non_defini(self):
        url = reverse('batiment_search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, batiment.PAGE_LISTE_BATIMENTS)

    def test_create(self):
        url = reverse('batiment-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, pages_utils.PAGE_BATIMENT_FORM)

    def test_batiment_form(self):
        un_batiment = BatimentFactory(localite=self.localite_1)
        url = reverse('batiment', args=[un_batiment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, pages_utils.PAGE_BATIMENT_FORM)
        self.assertEqual(response.context['batiment'], un_batiment)
        self.assertEqual(len(response.context['localites']), 2)
        self.assertEqual(len(response.context['assurances']), 2)

    def test_is_update_action(self):
        self.assertTrue(batiment._is_updating_action(pages_utils.ADD))
        self.assertTrue(batiment._is_updating_action(pages_utils.MODIFY))
        self.assertFalse(batiment._is_updating_action("qui_sait"))
        self.assertFalse(batiment._is_updating_action(None))

    def test_get_field(self):
        self.assertIsNone(batiment._get_field('champ11', {'champ1': 'valeur champ1'}))
        self.assertEquals(batiment._get_field('champ1', {'champ1': 'valeur champ1'}), 'valeur champ1')

    def test_get_localite(self):
        nouvelle_localite = batiment._get_localite({'localite_cp': '5000',
                                                    'localite_nom': 'Namur'})
        self.assertEquals(nouvelle_localite.code_postal, "5000")
        self.assertEquals(nouvelle_localite.localite, "Namur")

        une_localite_existante = batiment._get_localite({'localite_cp': nouvelle_localite.code_postal,
                                                         'localite_nom': nouvelle_localite.localite})
        self.assertEquals(nouvelle_localite.code_postal, "5000")
        self.assertEquals(nouvelle_localite.localite, "Namur")

    def test_get_batiment(self):
        un_batiment = BatimentFactory(localite=self.localite_1)
        self.assertEqual(batiment._get_batiment({'id': un_batiment.id}), un_batiment)
        self.assertIsNone(batiment._get_batiment({'id': None}).id)


# @mock.patch('django.contrib.auth.decorators')
    # @mock.patch('main.layout.render')
    # def test_search_par_proprietaire(self, mock_render, mock_decorators):
    #     print('test_search_par_proprietaire')
    #     mock_decorators.login_required = lambda x: x
    #     personne_1 = factory.SubFactory(PersonneFactory)
    #     gestionnaire = factory.SubFactory(PersonneFactory)
    #     batiment_1 = BatimentFactory()
    #     proprietaire_1 = ProprietaireFactory(proprietaire=factory.SubFactory(PersonneFactory), batiment=BatimentFactory())
    #
    #     personne_2 = factory.SubFactory(PersonneFactory)
    #     batiment_2 = BatimentFactory()
    #     proprietaire_2 = ProprietaireFactory(proprietaire=personne_2, batiment=batiment_2)
    #     request_factory = RequestFactory()
    #     request = request_factory.get(reverse('batiment_search'))
    #     request.proprietaire = proprietaire_2.id
    #     request.user = mock.Mock()
    #
    #     from main import batiment
        #
        # response =  batiment.search_par_proprietaire(request)
        # self.assertEqual(response.status_code, 200)
        #
        #
        # self.assertTemplateUsed(response, batiment.PAGE_LISTE_BATIMENTS)
        #

        # self.assertTrue(mock_render.called)
        # request, template, context = mock_render.call_args[0]
        # self.assertEqual(template, batiment.PAGE_LISTE_BATIMENTS)

def creer_5_batiments_avec_proprio(une_localite):
    cpt = 0
    while cpt < 5:
        un_batiment = BatimentFactory(localite=une_localite)
        un_proprio = ProprietaireFactory(batiment=un_batiment)
        cpt = cpt + 1

