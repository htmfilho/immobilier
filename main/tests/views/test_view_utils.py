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
from main import views_utils
from django.test import TestCase


class ViewUtilsTest(TestCase):

    def test_get_key_none(self):
        self.assertIsNone(views_utils.get_key(None))
        self.assertIsNone(views_utils.get_key("-"))
        self.assertIsNone(views_utils.get_key("None"))

    def test_get_key_int(self):
        self.assertEqual(views_utils.get_key("2"),2)
        self.assertEqual(views_utils.get_key(2),2)
