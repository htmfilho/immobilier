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
from django.utils import timezone
from main.models import honoraire as mdl_honoraire
from main.tests.factories.honoraire import HonoraireFactory
from main.models.enums import etat_honoraire
from dateutil.relativedelta import relativedelta


class HonoraireTest(TestCase):

    def test_find_honoraires_by_etat_today_with_results(self):
        etat_cherche = etat_honoraire.A_VERIFIER

        honoraire_1 = HonoraireFactory(date_paiement=timezone.now(),
                                       etat=etat_cherche)

        self.assertCountEqual(mdl_honoraire.find_honoraires_by_etat_today(etat_cherche), [honoraire_1])
        self.assertCountEqual(mdl_honoraire.find_honoraires_by_etat_today(etat_honoraire.IMPAYE), [])

    def test_find_honoraires_by_etat_today_no_result(self):
        HonoraireFactory(date_paiement=timezone.now(),
                         etat=etat_honoraire.A_VERIFIER)

        self.assertCountEqual(mdl_honoraire.find_honoraires_by_etat_today(etat_honoraire.IMPAYE), [])

    def test_find_honoraires_by_etat_today_no_result_out_of_period(self):
        honoraire_1 = HonoraireFactory(date_paiement=timezone.now() - relativedelta(months=8))

        self.assertCountEqual(mdl_honoraire.find_honoraires_by_etat_today(honoraire_1.etat), [])

    def test_find_all(self):
        honoraire_1 = HonoraireFactory(date_paiement=timezone.now())
        honoraire_2 = HonoraireFactory(date_paiement=timezone.now())

        self.assertCountEqual(mdl_honoraire.find_all(), [honoraire_1, honoraire_2])

    def test_find_by_batiment_etat_date_no_args(self):
        HonoraireFactory(date_paiement=timezone.now())
        HonoraireFactory(date_paiement=timezone.now())
        self.assertEquals(len(mdl_honoraire.find_by_batiment_etat_date(None, None, None, None)), 2)

    def test_find_by_batiment_etat_date(self):
        HonoraireFactory(date_paiement=timezone.now(), etat=etat_honoraire.A_VERIFIER)
        HonoraireFactory(date_paiement=timezone.now(), etat=etat_honoraire.EN_RETARD)
        self.assertEquals(len(mdl_honoraire.find_by_batiment_etat_date(None, etat_honoraire.A_VERIFIER, None, None)), 1)
