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
from django.utils import timezone
import datetime
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

    def test_date_is_valide(self):
        un_proprietaire = ProprietaireFactory(date_debut=datetime.date(timezone.now().year, 1, 1),
                            date_fin=datetime.date(timezone.now().year, 1, 3))

        self.assertTrue(proprietaire_view._date_is_valide(un_proprietaire))

    def test_date_is_not_valide(self):
        un_proprietaire = ProprietaireFactory(date_debut=datetime.date(timezone.now().year, 1, 1),
                                              date_fin=datetime.date(timezone.now().year-1, 1, 1))

        self.assertFalse(proprietaire_view._date_is_valide(un_proprietaire))

    def test_no_existing_prorietaire_selected(self):
        self.assertTrue(proprietaire_view._no_existing_prorietaire_selected("-"))
        self.assertTrue(proprietaire_view._no_existing_prorietaire_selected(None))

    def test_existing_prorietaire_selected(self):
        self.assertFalse(proprietaire_view._no_existing_prorietaire_selected(1))

    def test_new_parameters_ok(self):
        self.assertTrue(proprietaire_view._new_parameters_ok('Nom', 'Prénom'))

    def test_new_parameters_ko(self):
        self.assertFalse(proprietaire_view._new_parameters_ok('Nom', None))
        self.assertFalse(proprietaire_view._new_parameters_ok(None, 'Olivier'))
        self.assertFalse(proprietaire_view._new_parameters_ok(None, None))
        self.assertFalse(proprietaire_view._new_parameters_ok(' ', ' '))


    def test_form_validation(self):

        un_proprietaire = ProprietaireFactory()
        data = {'proprietaire': un_proprietaire.id}
        self.assertIsNone(proprietaire_view._validation(data, un_proprietaire))
        data = {'proprietaire': None,
         'nouveau_nom': None,
         'nouveau_prenom': None,
         'nouveau_prenom2': None,
         }
        self.assertEqual(proprietaire_view._validation(data, un_proprietaire), proprietaire_view.MESSAGE_CREE_UNE_NOUVELLE_PERSONNE)
        une_personnne = PersonneFactory(nom='Dupont',
                                        prenom='Hervé')

        data = {'proprietaire': None,
                'nouveau_nom': une_personnne.nom,
                'nouveau_prenom': une_personnne.prenom,
                'nouveau_prenom2': une_personnne.prenom2,
                }
        self.assertIsNotNone(proprietaire_view._validation(data, un_proprietaire))


        data = {'proprietaire': None,
                'nouveau_nom': une_personnne.nom + "z",
                'nouveau_prenom': une_personnne.prenom + "z",
                'nouveau_prenom2': une_personnne.prenom2 + "Z",
                }
        self.assertIsNone(proprietaire_view._validation(data, un_proprietaire))
