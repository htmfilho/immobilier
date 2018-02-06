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
from django.core.urlresolvers import reverse
from main.tests.factories.suivi_loyer import SuiviLoyerFactory
from main.tests.factories.financement_location import FinancementLocationFactory
from django.utils import timezone
from main.models import suivi_loyer as mdl_suivi_loyer
from main import suivis as suivis_view
from main import societe as societe_view


class SocieteViewTest(TestCase):

    def test_redirection_next_nav_personne_liste(self):
        response  = societe_view.redirection_next_nav(societe_view.NEXT_NAV_PERSONNE_LIST)
        self.assertEqual(response.url, '/personnes/')

    def test_redirection_next_nav_societe_liste(self):
        response  = societe_view.redirection_next_nav(societe_view.NEXT_NAV_SOCIETE_LIST)
        self.assertEqual(response.url, '/societes/')