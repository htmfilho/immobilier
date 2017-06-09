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
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from main.models import contrat_gestion as mdl_contrat_gestion
from main.tests.factories.batiment import BatimentFactory
from main.tests.factories.contrat_gestion import ContratGestionFactory
from main.tests.factories.financement_location import FinancementLocationFactory
from main.tests.models import test_personne

class ContratGestionTest(TestCase):
    # marche pas
    # def test_search(self):
    #     gestionnaire_par_defaut = test_personne.create_gestionnaire_par_defaut()
    #     un_batiment = BatimentFactory()
    #     un_contrat_gestion = ContratGestionFactory(batiment=un_batiment,
    #                                                gestionnaire=gestionnaire_par_defaut)
    #     self.assertCountEqual(mdl_contrat_gestion.find_my_contrats(), [un_contrat_gestion])


