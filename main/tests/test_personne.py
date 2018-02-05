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


class PersonneViewTest(TestCase):

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

