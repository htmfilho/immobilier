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
from main.models.enums import alerte_etat
from main.models import alerte as mdl_alerte
from main.tests.factories.alerte import AlerteFactory


class AlerteTest(TestCase):

    def test_find_by_etat_no_data(self):
        self.assertCountEqual(mdl_alerte.find_by_etat(alerte_etat.A_VERIFIER), [])


    def test_find_by_etat(self):
        une_alerte_a_verifier = AlerteFactory(etat=alerte_etat.A_VERIFIER)
        self.assertCountEqual(mdl_alerte.find_by_etat(alerte_etat.A_VERIFIER), [une_alerte_a_verifier])


    def test_find_by_etat_today_no_data(self):
        date_avant_periode_recherche = timezone.now() - relativedelta(months=2)
        une_alerte_a_verifier = AlerteFactory(etat=alerte_etat.A_VERIFIER,
                                              date_alerte=date_avant_periode_recherche)
        self.assertCountEqual(mdl_alerte.find_by_etat_today(alerte_etat.A_VERIFIER), [])

    def test_find_by_etat_today(self):
        une_alerte_a_verifier = AlerteFactory(etat=alerte_etat.A_VERIFIER,
                                              date_alerte=timezone.now())
        self.assertCountEqual(mdl_alerte.find_by_etat_today(alerte_etat.A_VERIFIER), [une_alerte_a_verifier])

