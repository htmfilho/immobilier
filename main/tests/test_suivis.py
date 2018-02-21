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
from django.test.client import Client
from django.contrib.auth.models import User


class SuivisViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.financement = FinancementLocationFactory(date_debut=timezone.now(),
                                                      date_fin=timezone.now(),
                                                      loyer=150,
                                                      charges=20,
                                                      index=21)
        self.suivi = SuiviLoyerFactory(financement_location=self.financement,
                                       etat_suivi='A_VERIFIER')

    def test_update_suivi_no_data_id_in_post(self):
        no_data = {}
        url = reverse('update_suivi')
        response = self.client.post(url, no_data)
        self.assertEqual(response.status_code, 404)
    #
    # def test_update_suivi_modification_montants_non_precises(self):
    #     data = {'id': self.suivi.id}
    #     url = reverse('update_suivi')
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEquals(mdl_suivi_loyer.SuiviLoyer.objects.get(pk=self.suivi.id).loyer_percu, 0)
    #     self.assertEquals(mdl_suivi_loyer.SuiviLoyer.objects.get(pk=self.suivi.id).charges_percu, 0)
    #
    #     self.assertTemplateUsed(response, suivis_view.SUIVI_SUIVIS_HTML)
