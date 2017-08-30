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
from main.models import suivi_loyer as mdl_suivi_loyer
from main.tests.factories.personne import PersonneFactory
from main.tests.factories.suivi_loyer import SuiviLoyerFactory
import operator


# class SuiviLoyerTest(TestCase):

    # def test_find_suivis(self):
        # print('iii')
        # suivi_1 = SuiviLoyerFactory()
        # print('iii2')
        # self.assertCountEqual(mdl_suivi_loyer.find_all(), [suivi_1])
