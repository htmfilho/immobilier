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
from main.tests.factories.suivi_loyer import SuiviLoyerFactory
from main.tests.factories.financement_location import FinancementLocationFactory
from django.utils import timezone
from main.models.enums import etat_suivi
from main import views
from main.tests.factories.frais_maintenance import FraisMaintenanceFactory


class ViewsTest(TestCase):

    def setUp(self):
        self.financement = FinancementLocationFactory(date_debut=timezone.now(),
                                                      date_fin=timezone.now(),
                                                      loyer=500,
                                                      charges=200,
                                                      index=21)
        self.suivi1 = SuiviLoyerFactory(financement_location=self.financement,
                                        etat_suivi=etat_suivi.PAYE,
                                        loyer_percu=self.financement.loyer,
                                        charges_percu=self.financement.charges)
        self.suivi2 = SuiviLoyerFactory(financement_location=self.financement,
                                        etat_suivi=etat_suivi.PAYE,
                                        loyer_percu=self.financement.loyer,
                                        charges_percu=self.financement.charges)

    def test_get_total_recettes(self):
        self.assertEqual(views._get_total_recettes([self.suivi1, self.suivi2]), 1400)
        self.suivi2.charges_percu = 0
        self.assertEqual(views._get_total_recettes([self.suivi1, self.suivi2]), 1200)

    def test_get_total_recettes_equals_zero(self):
        self.assertEqual(views._get_total_recettes(None), 0)
        self.assertEqual(views._get_total_recettes([]), 0)

    def test_sum_recette(self):
        self.assertEqual(views._get_montant_to_add(None), 0)
        self.assertEqual(views._get_montant_to_add(0), 0)
        self.assertEqual(views._get_montant_to_add(100), 100)

    def test_get_total_depenses(self):
        frais_1 = FraisMaintenanceFactory(montant=150)
        frais_2 = FraisMaintenanceFactory(montant=300)

        self.assertEqual(views._get_total_depenses([frais_1, frais_2]), 450)

        frais_2 = FraisMaintenanceFactory(montant=0)

        self.assertEqual(views._get_total_depenses([frais_1, frais_2]), 150)
        self.assertEqual(views._get_total_depenses([]), 0)
        self.assertEqual(views._get_total_depenses(None), 0)
