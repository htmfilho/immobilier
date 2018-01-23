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
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from main import alertes
from main.tests.factories.alerte import AlerteFactory
from main.models.enums import alerte_etat
from main import models as mdl


class AlertesViewTest(TestCase):

    def setUp(self):
        self.alerte_a_verifier = AlerteFactory(etat=alerte_etat.VERIFIER)
        self.alerte_courrier = AlerteFactory(etat=alerte_etat.COURRIER)

    def test_list_default(self):
        etat_cherche_par_defaut = alerte_etat.VERIFIER
        expected_objects = [self.alerte_a_verifier]

        url = reverse('alerte-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, alertes.PAGE_ALERTE_LIST)
        self.assertEqual(list(response.context['alertes']), expected_objects)
        self.assertEqual(response.context['etat_alerte'], etat_cherche_par_defaut)

    def test_save_alerte_a_verifier(self):
        alertes.save_alerte_a_verifier(self.alerte_courrier.id)
        self.assertEqual(mdl.alerte.Alerte.objects.get(pk=self.alerte_courrier.pk).etat,
                         alerte_etat.VERIFIER)

    def test_render_alert_avec_etat(self):
        url = reverse('alerte-search')
        response = self.client.get(url,  {'etat_alerte': alerte_etat.VERIFIER})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, alertes.PAGE_ALERTE_LIST)
        self.assertEqual(response.context['alertes'].count(), 1)

    def test_render_alert_sans_etat(self):
        url = reverse('alerte-search')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, alertes.PAGE_ALERTE_LIST)
        self.assertEqual(response.context['alertes'].count(), 2)
