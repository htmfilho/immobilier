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
import datetime
from django.test import TestCase
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from main.models import frais_maintenance as mdl_frais_maintenance
from main.tests.factories.batiment import BatimentFactory
from main.tests.factories.frais_maintenance import FraisMaintenanceFactory
from main.tests.factories.proprietaire import ProprietaireFactory
from main.tests.factories.contrat_location import ContratLocationFactory
from main.tests.models import test_personne


class FraisMaintenanceTest(TestCase):

    def test_find_by_batiment(self):
        un_batiment = BatimentFactory()
        frais_1 = FraisMaintenanceFactory(batiment=un_batiment)
        frais_2 = FraisMaintenanceFactory(batiment=un_batiment)
        self.assertCountEqual(mdl_frais_maintenance.find_by_batiment(un_batiment), [frais_1, frais_2])

    def test_find_mes_frais_du_mois(self):
        gestionnaire = test_personne.create_gestionnaire_par_defaut()
        un_batiment = BatimentFactory()
        a_proprio = ProprietaireFactory(proprietaire=gestionnaire,
                                        batiment=un_batiment)
        frais_1 = FraisMaintenanceFactory(batiment=un_batiment,
                                          contrat_location=None,
                                          date_realisation=datetime.datetime(timezone.now().year, timezone.now().month, 1))

        frais_2 = FraisMaintenanceFactory(batiment=un_batiment,
                                          contrat_location=None,
                                          date_realisation=datetime.datetime(timezone.now().year, timezone.now().month, 2))

        self.assertCountEqual(mdl_frais_maintenance.find_mes_frais_du_mois(), [frais_1, frais_2])

    def test_find_by_contrat_location(self):
        contrat_location = ContratLocationFactory()
        frais_1 = FraisMaintenanceFactory(contrat_location=contrat_location)
        self.assertCountEqual(mdl_frais_maintenance.find_by_contrat_location(contrat_location.id), [frais_1])

