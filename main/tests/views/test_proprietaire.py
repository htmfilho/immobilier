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
from rest_framework.reverse import reverse
from main.tests.factories.proprietaire import ProprietaireFactory
from main.tests.factories.type_societe import TypeSocieteFactory
from django.contrib.auth.models import User
from main.pages_utils import PAGE_PROPRIETAIRE_FORM


class ProprietaireTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('tmp', 'tmp@gmail.com', 'tmp')
        self.client.force_login(self.user)
        self.proprietaire = ProprietaireFactory()
        self.type_societe_1 = TypeSocieteFactory()
        self.type_societe_2 = TypeSocieteFactory()

    def test_proprietaire(self):
        url = reverse('proprietaire', kwargs={'proprietaire_id': self.proprietaire.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, PAGE_PROPRIETAIRE_FORM)
        self.assertCountEqual(response.context['type_societes'], [self.type_societe_1, self.type_societe_2])
