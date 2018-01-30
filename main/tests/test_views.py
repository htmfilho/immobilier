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
from main.tests.factories.batiment import BatimentFactory
from django.utils import timezone
from main.models.enums import etat_suivi
from main import views
from main.tests.factories.frais_maintenance import FraisMaintenanceFactory
from main.tests.factories.proprietaire import ProprietaireFactory
from main.tests.factories.personne import PersonneFactory
from main.tests.factories.contrat_location import ContratLocationFactory
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.auth.models import User
from main import models as mdl

class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        batiment_contrat = BatimentFactory()
        self.batiment_1 = BatimentFactory()
        self.batiment_2 = BatimentFactory()
        self.batiment_3 = BatimentFactory()
        self.contrat_location = ContratLocationFactory(batiment=batiment_contrat)
        self.financement = FinancementLocationFactory(date_debut=timezone.now(),
                                                      date_fin=timezone.now(),
                                                      loyer=500,
                                                      charges=200,
                                                      index=21,
                                                      contrat_location=self.contrat_location)
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

    def test_listeBatiments(self):
        personne_1 = PersonneFactory()
        personne_2 = PersonneFactory()

        proprietaire_a = ProprietaireFactory(batiment=self.batiment_1,
                                             proprietaire=personne_1)
        proprietaire_b = ProprietaireFactory(batiment=self.batiment_2,
                                             proprietaire=personne_2)
        proprietaire_c = ProprietaireFactory(batiment=self.batiment_3,
                                             proprietaire=personne_2)
        url = reverse('listeBatiments')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, views.PAGE_LISTE_BATIMENTS)
        self.assertEqual(response.context['batiments'].count(), mdl.batiment.Batiment.objects.all().count())
