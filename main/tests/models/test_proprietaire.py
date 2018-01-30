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
from main.tests.factories.personne import PersonneFactory
from main.tests.factories.proprietaire import ProprietaireFactory
from main.tests.factories.batiment import BatimentFactory
from main import models as mdl


class ProprietaireTest(TestCase):

    def setUp(self):
        self.personne_1 = PersonneFactory(nom="Dupuis")
        self.personne_2 = PersonneFactory(nom="Allard")
        self.personne_3 = PersonneFactory(nom="Bertrand")

        self.batiment_1 = BatimentFactory()
        self.batiment_2 = BatimentFactory()
        self.batiment_3 = BatimentFactory()
        self.batiment_4 = BatimentFactory()

        self.proprietaire_1 = ProprietaireFactory(proprietaire=self.personne_1,
                                                  batiment=self.batiment_1)
        self.proprietaire_2 = ProprietaireFactory(proprietaire=self.personne_2,
                                                  batiment=self.batiment_2)

        self.proprietaire_3 = ProprietaireFactory(proprietaire=self.personne_2,
                                                  batiment=self.batiment_3)

    def test_find_distinct_proprietaires(self):
        self.assertEqual(len(mdl.proprietaire.find_distinct_proprietaires()), 2)

    def test_find_distinct_proprietaires_order(self):
        self.assertEqual(list(mdl.proprietaire.find_distinct_proprietaires()),
                         [self.proprietaire_2, self.proprietaire_1])

    def test_find_batiment_by_personne(self):
        self.assertEqual(len(mdl.proprietaire.find_batiment_by_personne(self.personne_2)), 2)

    def test_find_batiment_by_personne_no_result(self):
        self.assertEqual(len(mdl.proprietaire.find_batiment_by_personne(self.personne_3)), 0)

    def test_find_all(self):
        self.assertCountEqual(mdl.proprietaire.find_all(),
                              [self.proprietaire_2, self.proprietaire_3, self.proprietaire_1])

    def test_find_by_batiment(self):
        self.assertCountEqual(mdl.proprietaire.find_by_batiment(self.batiment_1),
                              [self.proprietaire_1])

    def test_find_by_batiment_no_proprio(self):
        self.assertCountEqual(mdl.proprietaire.find_by_batiment(self.batiment_4),
                              [])

    def test_find_by_personne(self):
        self.assertEqual(len(mdl.proprietaire.find_by_personne(self.personne_2)), 2)

    def test_search(self):
        self.assertEqual(len(mdl.proprietaire.search(None, None)), 3)
        self.assertEqual(len(mdl.proprietaire.search(self.personne_2, None)), 2)
        self.assertEqual(len(mdl.proprietaire.search(None, self.batiment_1)), 1)
        self.assertEqual(len(mdl.proprietaire.search(self.personne_3, self.batiment_1)), 0)
