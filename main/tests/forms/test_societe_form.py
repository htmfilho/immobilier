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
from main.forms.societe_form import SocieteForm
from django.test import TestCase
from main.tests.factories.batiment import BatimentFactory
from main.tests.factories.personne import GestionnairePersonneFactory, PersonneFactory


class SocieteFormTest(TestCase):

    def setUp(self):
        self.gestionnaire = GestionnairePersonneFactory()
        self.personne_non_gestionnaire = PersonneFactory()
        self.personne_non_gestionnaire = PersonneFactory()

    def test_init_required_field(self):
        form = SocieteForm()
        self.assertTrue(form.fields['nom'].required)

    def test_valid(self):
        form = SocieteForm({'nom': None})
        self.assertFalse(form.is_valid(), form.errors)
