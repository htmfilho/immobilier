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
from main.models import localite as mdl_localite
from main.tests.factories.localite import LocaliteFactory


class LocaliteTest(TestCase):

    def test_search(self):
        a_cp_param = "5001"
        a_localite_param = "Lisogne"

        a_localite = LocaliteFactory(code_postal=a_cp_param, localite=a_localite_param)

        self.assertCountEqual(mdl_localite.search(a_cp_param, a_localite_param), [a_localite])

    def test_find_by_id(self):
        a_localite = LocaliteFactory()
        self.assertEqual(mdl_localite.find_by_id(a_localite.id), a_localite)

