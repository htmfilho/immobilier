#############################################################################
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
from main import societe as societe_view
from main.tests.factories.societe import SocieteFactory
from main.tests.factories.type_societe import TypeSocieteFactory
from main.forms.societe_form import SocieteForm
from main.models.societe import Societe


class SocieteViewTest(TestCase):

    def setUp(self):
        self.societe_1 = SocieteFactory(nom="Brantano")
        self.societe_2 = SocieteFactory(nom="Allard")

        self.type_societe = TypeSocieteFactory(type="Macon")

    def test_redirection_next_nav_personne_liste(self):
        response = societe_view.redirection_next_nav(societe_view.NEXT_NAV_PERSONNE_LIST)
        self.assertEqual(response.url, '/personnes/')

    def test_redirection_next_nav_societe_liste(self):
        response = societe_view.redirection_next_nav(societe_view.NEXT_NAV_SOCIETE_LIST)
        self.assertEqual(response.url, '/societes/')

    def test_liste(self):
        response = self.client.get(
            reverse("societe-list")
        )
        self.assertTemplateUsed(response, 'societe/societe_list.html')

        self.assertCountEqual(response.context['societes'], [self.societe_1, self.societe_2])
        self.assertEqual(response.context['societes'][0], self.societe_2)
        self.assertEqual(response.context['societes'][1], self.societe_1)

    def test_new_get_from_list(self):
        response = self.client.get(
            reverse("societe_new")
        )

        self.assertTemplateUsed(response, 'societe/societe_form.html')
        self.assertIsInstance(response.context['form'], SocieteForm)

    def test_new_post_from_list(self):
        response = self.client.post(
            reverse("societe_new"), data={'nom': 'Test'}
        )
        self.assertRedirects(response, reverse('societe-list'))

    def test_get_societe(self):
        self.assertEqual(societe_view.get_societe(self.societe_1.id), self.societe_1)
        societe = societe_view.get_societe(None)
        self.assertIsNone(societe.id)
        self.assertEqual(societe.nom, '')

    def test_get_type_societe(self):
        self.assertIsNone(societe_view._get_type_societe(None, None))
        self.assertEqual(societe_view._get_type_societe(None, self.type_societe.id), self.type_societe)
        self.assertEqual(societe_view._get_type_societe(None, 99999), None)

    def test_creation_nouvelle_societe(self):
        nouvelle_societe = societe_view.creation_nouvelle_societe("Nouvelle", "Une description")
        self.assertEqual(nouvelle_societe.nom, "Nouvelle")
        self.assertEqual(nouvelle_societe.description, "Une description")