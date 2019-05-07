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
from main import contratgestion
from main.tests.factories.batiment import BatimentFactory
from main.tests.factories.contrat_gestion import ContratGestionFactory
from main import pages_utils
from django.forms import model_to_dict
from django.test.client import Client
from django.contrib.auth.models import User
from main.tests.factories.personne import GestionnairePersonneFactory
from main.pages_utils import NEW
from django.http import HttpResponseNotFound


class ContratGestionViewLoginRequiredTest(TestCase):

    def setUp(self):
        self.batiment_1 = BatimentFactory()
        self.contrat_gestion_1 = ContratGestionFactory(batiment=self.batiment_1)

    def test_login(self):
        url = reverse("gestion-prepare-update-all", args=[self.contrat_gestion_1.id]),
        response = self.client.post(
            url
        )

        self.assertEqual(response.status_code, HttpResponseNotFound.status_code)


class ContratGestionViewTest(TestCase):

    def setUp(self):
        self.batiment_1 = BatimentFactory()
        self.contrat_gestion_1 = ContratGestionFactory(batiment=self.batiment_1)
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.gestionnaire = GestionnairePersonneFactory()

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

    def test_update(self):
        post_data = model_to_dict(self.contrat_gestion_1)
        post_data['date_debut'] = '01/05/2018'
        post_data['date_fin'] = '01/05/2019'
        post_data['action'] = 'update'
        post_data['gestionnaire'] = self.gestionnaire.id
        nouveau_montant_mensuel = post_data.get('montant_mensuel', 0) + 100
        post_data['montant_mensuel'] = nouveau_montant_mensuel

        response = self.client.post(
            reverse("update-gestion-all"), data=post_data
        )
        self.assertEqual(response.context['contrat_de_gestion'].montant_mensuel, nouveau_montant_mensuel)

    def test_update_2(self):
        response = self.client.post(
            reverse("gestion-create-update",
                    kwargs={'id_contrat': self.contrat_gestion_1.id}),

        )

        self.assertTemplateUsed(response, 'gestion/update.html')

    def test_update_invalid_form(self):
        post_data = model_to_dict(self.contrat_gestion_1)
        post_data['date_debut'] = '01/05/2018'
        post_data['date_fin'] = '01/05/2017'

        response = self.client.post(
            reverse("update-gestion-all"), data=post_data
        )
        self.assertEqual(response.context['id_contrat'], post_data['id'])
        self.assertTemplateUsed(response, 'gestion/update.html')

    def test_new(self):
        post_data = {
            'date_debut': '01/05/2018',
            'date_fin': '01/05/2019',
            'action': 'update',
            'gestionnaire': self.gestionnaire.id,
            'batiment': self.contrat_gestion_1.batiment.id,
            'montant_mensuel': 100
        }
        response = self.client.post(
            reverse("update-gestion-all"), data=post_data
        )
        self.assertEqual(response.context['contrat_de_gestion'].montant_mensuel, 100)

    def test_new_from_home(self):
        response = self.client.post(
            reverse("contratgestion-new")
        )
        self.assertTemplateUsed(response, 'gestion/create.html')
        self.assertEqual(response.context['action'], NEW)

    def test_new_from_batiment(self):
        response = self.client.get(
            reverse("contratgestion-create", args=[self.batiment_1.id]),


        )

        self.assertTemplateUsed(response, 'gestion/create.html')
        self.assertEqual(response.context['batiment'], self.batiment_1)

    def test_new_from_batiment_for_default_gestionnaire(self):
        response = self.client.get(
            reverse("contratgestion-create", args=[self.batiment_1.id]),


        )

        self.assertTemplateUsed(response, 'gestion/create.html')
        self.assertEqual(response.context['batiment'], self.batiment_1)
        self.assertEqual(response.context['contrat'].gestionnaire, self.gestionnaire)

    def test_create(self):
        post_data = {

            'date_debut': '01/05/2018',
            'date_fin': '01/05/2019',

            'gestionnaire': self.gestionnaire.id,
            'batiment': self.contrat_gestion_1.batiment.id,
            'montant_mensuel': 100
        }
        response = self.client.post(
            reverse("contratgestion-create", args=[self.batiment_1.id]),
            data=post_data

        )

        self.assertTemplateUsed(response, pages_utils.PAGE_BATIMENT_FORM)
        self.assertEqual(response.context['batiment'].id, self.contrat_gestion_1.batiment.id)

    def test_prepare_update(self):
        response = self.client.get(
            reverse("gestion-prepare-update-all", args=[self.contrat_gestion_1.id]),
        )

        self.assertTemplateUsed(response, 'gestion/update.html')

        self.assertEqual(response.context['contrat'], self.contrat_gestion_1)

