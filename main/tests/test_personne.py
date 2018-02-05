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
from main.tests.factories.type_societe import TypeSocieteFactory
from main import personne as personne_view
from django.test.client import Client
from django.contrib.auth.models import User
from main.tests.factories.fonction import FonctionFactory
from main.tests.factories.pays import PaysFactory


class PersonneViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')


    def test_list(self):

        personne_1 = PersonneFactory(nom="Allard")
        personne_2 = PersonneFactory(nom="Dupuis")
        url = reverse('personne_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, personne_view.PERSONNE_LIST_HTML)
        self.assertCountEqual(response.context['personnes'], [personne_1, personne_2])

    def test_list_order(self):

        personne_1 = PersonneFactory(nom="Allard")
        personne_2 = PersonneFactory(nom="Dupuis")
        personne_3 = PersonneFactory(nom="Bastin")
        url = reverse('personne_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, personne_view.PERSONNE_LIST_HTML)

        self.assertCountEqual(response.context['personnes'], [personne_1, personne_2, personne_3])
        expected_order = [personne_1, personne_3, personne_2]
        self.assertEqual(response.context['personnes'][0], expected_order[0])
        self.assertEqual(response.context['personnes'][1], expected_order[1])
        self.assertEqual(response.context['personnes'][2], expected_order[2])

    def test_get_common_data_for_creation(self):
        personne_1 = PersonneFactory()
        data = personne_view.get_common_data(personne_1.id)
        self.assertEqual(data.get('personne'), personne_1)

    def test_get_common_data_for_update(self):
        data = personne_view.get_common_data(None)
        self.assertIsNone(data.get('personne').id)

    def test_get_common_data_for_dropdown(self):

        cpt = 0
        while cpt < 5:
            FonctionFactory(nom_fonction="Fonction {}".format(cpt))
            PaysFactory()
            LocaliteFactory(pays=None)
            TypeSocieteFactory()
            SocieteFactory(type=None, localite=None)
            cpt += 1

        data = personne_view.get_common_data(None)
        self.assertEqual(data.get('fonctions').count(), 5)
        self.assertEqual(data.get('societes').count(), 5)
        self.assertEqual(data.get('pays').count(), 5)
        self.assertEqual(data.get('localites').count(), 5)
        self.assertEqual(data.get('type_societes').count(), 5)

    def test_get_personne(self):
        personne_1 = PersonneFactory()
        self.assertEqual(personne_view.get_personne(personne_1.id), personne_1)

    def test_get_personne(self):
        personne_1 = PersonneFactory()
        result = personne_view.get_personne(None)
        self.assertIsNone(result.id)

    def test_edit(self):

        personne_1 = PersonneFactory(nom="Allard")
        url = reverse('personne-edit',args=[personne_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, personne_view.PERSONNE_FORM_HTML)
        self.assertEqual(response.context['personne'], personne_1)

    def test_create(self):
        url = reverse('personne-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, personne_view.PERSONNE_FORM_HTML)
        self.assertIsNone(response.context['personne'].id)


    def test_search(self):
        un_nom = "Allard"
        un_prenom = "Marie"
        un_prenom_compose = "Marie-Claire"
        personne_1 = PersonneFactory(nom=un_nom, prenom=un_prenom)
        personne_2 = PersonneFactory(nom=un_nom, prenom=un_prenom_compose)
        url = reverse('personne_search')

        response = self.client.get(url, data={"nom": un_nom, "prenom": un_prenom})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, personne_view.PERSONNE_LIST_HTML)
        self.assertCountEqual(response.context['personnes'], [personne_1, personne_2])
        self.assertEqual(response.context['nom'], un_nom)
        self.assertEqual(response.context['prenom'], un_prenom)

        response = self.client.get(url, data={"nom": un_nom, "prenom": un_prenom_compose})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, personne_view.PERSONNE_LIST_HTML)
        self.assertCountEqual(response.context['personnes'], [personne_2])
        self.assertEqual(response.context['nom'], un_nom)
        self.assertEqual(response.context['prenom'], un_prenom_compose)


        response = self.client.get(url, data={"nom": un_nom})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, personne_view.PERSONNE_LIST_HTML)
        self.assertCountEqual(response.context['personnes'], [personne_1, personne_2])

        self.assertEqual(response.context['nom'], un_nom)
        self.assertIsNone(response.context['prenom'])

    def test_validate_personne_invalide_get(self):
        un_nom = "Louette"
        un_prenom = "Jules"
        un_prenom2 = "Ghislain"
        personne_1 = PersonneFactory(nom=un_nom, prenom=un_prenom, prenom2=un_prenom2)

        url = reverse('validate_personne')
        response = self.client.get(url, data={"nom": un_nom, "prenom": un_prenom, "prenom2": un_prenom2})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['valide'])

    def test_validate_personne_valide_get(self):
        un_nom = "Louette"
        un_prenom = "Jules"
        un_prenom2 = "Ghislain"
        personne_1 = PersonneFactory(nom=un_nom, prenom=un_prenom, prenom2=un_prenom2)

        url = reverse('validate_personne')
        response = self.client.get(url, data={"nom": un_nom, "prenom": "Juliette", "prenom2": un_prenom2})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['valide'])

    def test_validate_personne_invalide_post(self):
        un_nom = "Louette"
        un_prenom = "Jules"
        un_prenom2 = "Ghislain"
        personne_1 = PersonneFactory(nom=un_nom, prenom=un_prenom, prenom2=un_prenom2)

        url = reverse('validate_personne')
        response = self.client.post(url, data={"nom": un_nom, "prenom": un_prenom, "prenom2": un_prenom2})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['valide'])

    def test_validate_personne_valide_post(self):
        un_nom = "Louette"
        un_prenom = "Jules"
        un_prenom2 = "Ghislain"
        personne_1 = PersonneFactory(nom=un_nom, prenom=un_prenom, prenom2=un_prenom2)

        url = reverse('validate_personne')
        response = self.client.post(url, data={"nom": un_nom, "prenom": "Juliette", "prenom2": un_prenom2})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['valide'])

    def test_populate_profession(self):
        une_fonction = FonctionFactory(nom_fonction="Plombier")
        self.assertEqual(personne_view.populate_profession(une_fonction), "Plombier")

    def test_populate_profession_non_presente(self):
        self.assertIsNone(personne_view.populate_profession(None))

    def test_populate_date_non_presente(self):
        self.assertIsNone(personne_view.populate_date(None))

    def test_populate_date_non_formater(self):
        date_erronnee ="12//0282018"
        self.assertEqual(personne_view.populate_date(date_erronnee), date_erronnee)

    def test_populate_pays_non_precise(self):
        self.assertIsNone(personne_view.populate_pays_naissance(None))
        self.assertIsNone(personne_view.populate_pays_naissance(9))

    def test_populate_pays_precise(self):
        un_pays = PaysFactory()
        self.assertEqual(personne_view.populate_pays_naissance(un_pays.id), un_pays)