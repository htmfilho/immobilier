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
from main.models import batiment as mdl_batiment
from main.tests.factories.batiment import BatimentFactory
from main.tests.factories.personne import PersonneFactory
from main.tests.factories.proprietaire import ProprietaireFactory
from main.tests.models import test_personne


class BatimentTest(TestCase):

    def test_find_my_batiments(self):
        gestionnaire=test_personne.create_gestionnaire_par_defaut()
        un_batiment = BatimentFactory()
        un_proprio = ProprietaireFactory(proprietaire=gestionnaire,
                                         batiment=un_batiment)

        self.assertCountEqual(mdl_batiment.find_batiments_gestionnaire(),[un_batiment])

    def test_search_par_proprietaire(self):
        un_proprio = ProprietaireFactory()
        self.assertCountEqual(mdl_batiment.search_par_proprietaire(un_proprio.id),[un_proprio.batiment])

