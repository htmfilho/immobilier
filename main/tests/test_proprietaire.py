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
from main.tests.factories.batiment import BatimentFactory
from main.tests.factories.proprietaire import ProprietaireFactory
from main.tests.factories.personne import PersonneFactory
from main import proprietaire as proprietaire_view
from main.models.enums import etat_honoraire

class ProprietaireViewTest(TestCase):

    def test_liste_proprietaires(self):
        un_batiment = BatimentFactory()
        gestionnaire = PersonneFactory()
        ProprietaireFactory(proprietaire=gestionnaire,
                            batiment=un_batiment)
        url = reverse('listeProprietaires')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listeProprietaires.html')
        self.assertEqual(response.context['proprietaires'].count(), 1)

    def test_get_personnes_possibles(self):
        un_batiment = BatimentFactory()

        personne_proprietaire = PersonneFactory()
        ProprietaireFactory(proprietaire=personne_proprietaire,
                            batiment=un_batiment)

        PersonneFactory()
        PersonneFactory()

        self.assertEqual(len(proprietaire_view.get_personnes_possibles(un_batiment)), 2)
