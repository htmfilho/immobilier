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
from django.core.urlresolvers import reverse
from main.tests.factories.frais_maintenance import FraisMaintenanceFactory
from main.tests.factories.professionnel import ProfessionnelFactory
from main.tests.factories.honoraire import HonoraireFactory
from main.models.enums import alerte_etat
from main import models as mdl
from main import frais as frais_view
from main.tests.factories.personne import PersonneFactory
from main.models.enums import etat_honoraire
from main import honoraire as honoraire_view
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.utils import timezone


class HonoraireViewTest(TestCase):

    def test_list_default(self):
        date_limite = timezone.now() - relativedelta(days=15)
        date_limite_sup = timezone.now() + relativedelta(days=15)

        un_honoraire = HonoraireFactory(etat=honoraire_view.DEFAULT_ETAT_LIST,
                                        date_paiement=timezone.now())
        expected_objects = [un_honoraire]

        url = reverse('honoraire-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "honoraire/honoraire_list.html")
        self.assertEqual(list(response.context['honoraires']), expected_objects)

