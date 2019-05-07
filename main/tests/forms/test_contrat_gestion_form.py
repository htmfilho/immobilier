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
from main.forms.contrat_gestion import ContratGestionForm
from django.test import TestCase
from main.tests.factories.batiment import BatimentFactory
from main.tests.factories.personne import GestionnairePersonneFactory, PersonneFactory


class ContratGestionFormTest(TestCase):

    def setUp(self):
        self.gestionnaire = GestionnairePersonneFactory()
        self.personne_non_gestionnaire = PersonneFactory()
        self.personne_non_gestionnaire = PersonneFactory()

    def test_gestionnaires_list(self):
        form = ContratGestionForm()

        self.assertListEqual(list(form.fields['gestionnaire'].queryset),
                             [self.gestionnaire])

    def test_init_required_field(self):
        form = ContratGestionForm()

        self.assertTrue(form.fields['date_debut'].required)
        self.assertTrue(form.fields['date_fin'].required)
        self.assertTrue(form.fields['montant_mensuel'].required)
        self.assertTrue(form.fields['batiment'].required)
        self.assertTrue(form.fields['gestionnaire'].required)

    def test_date_checked(self):

        form = ContratGestionForm({'date_debut': '01/05/2019',
                                   'date_fin': '01/05/2018',
                                   'gestionnaire': self.gestionnaire.id,
                                   'montant_mensuel': 100,
                                   'batiment': BatimentFactory().id}
                                  )
        self.assertFalse(form.is_valid(), form.errors)
        self.assertEqual(form.errors['date_debut'][0],
                         'Dates erronées la date de début doit être inférieure à la date de fin')
