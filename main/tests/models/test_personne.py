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
from main.models import personne as mdl_personne
from main.models import fonction as mdl_fonction
from main.models import professionnel as mdl_professionnel
from main.tests.factories.personne import PersonneFactory
from main.tests.factories.fonction import FonctionFactory


NOM_DUPONT = "Dupont"
PRENOM_MARCEL = "Marcel"
PRENOM_GHISLAIN = "Ghislain"


class PersonneTest(TestCase):

    def test_find_gestionnaire_default_no_data(self):
        self.assertIsNone(mdl_personne.find_gestionnaire_default())
        une_personne = PersonneFactory(nom='Dupont')
        self.assertIsNone(mdl_personne.find_gestionnaire_default())
        une_personne_2 = PersonneFactory(nom=mdl_personne.NOM_GESTIONNAIRE,
                                         prenom='Antoine')
        self.assertIsNone(mdl_personne.find_gestionnaire_default())

    def test_find_gestionnaire_default(self):
        le_gestionnaire = create_gestionnaire_par_defaut()
        self.assertEquals(mdl_personne.find_gestionnaire_default(), le_gestionnaire)
        return le_gestionnaire

    def test_delete_impossible(self):
        self.assertFalse(mdl_personne.delete_personne(1))
        self.assertFalse(mdl_personne.delete_personne("1"))

    def test_delete_possible(self):
        une_personne = PersonneFactory()
        self.assertTrue(mdl_personne.delete_personne(une_personne.id))

    def test_find_personne_by_nom_prenom_with_nom_prenom_prenom2(self):
        une_personne = PersonneFactory(nom=NOM_DUPONT,
                                       prenom=PRENOM_MARCEL,
                                       prenom2=PRENOM_GHISLAIN)
        self.assertCountEqual(mdl_personne.find_personne_by_nom_prenom(NOM_DUPONT, PRENOM_MARCEL, PRENOM_GHISLAIN),
                              [une_personne])

    def test_search(self):
        une_personne = PersonneFactory(nom=NOM_DUPONT,
                                       prenom=PRENOM_MARCEL)
        self.assertCountEqual(mdl_personne.search(NOM_DUPONT, PRENOM_MARCEL), [une_personne])

    def test_creation_nouveau_professionnal_avec_nouvelle_fonction(self):
        nom_fonction_plombier = 'Plombier'
        une_personne = PersonneFactory(profession=nom_fonction_plombier)

        self.assertEquals(mdl_personne.find_personne(une_personne.id), une_personne)
        self.assertEquals(mdl_professionnel.find_by_personne(une_personne).first().personne,
                          une_personne)
        self.assertEquals(mdl_fonction.find_by_nom(nom_fonction_plombier).nom_fonction,
                          nom_fonction_plombier)

    def test_creation_nouveau_professionnal_sans_nouvelle_fonction(self):

        nom_fonction_plombier = 'Plombier'
        une_fonction = FonctionFactory(nom_fonction=nom_fonction_plombier)
        une_personne = PersonneFactory(fonction=une_fonction,
                                       profession=une_fonction.nom_fonction)

        self.assertEquals(mdl_personne.find_personne(une_personne.id), une_personne)
        self.assertEquals(mdl_professionnel.find_by_personne(une_personne).first().personne,
                          une_personne)
        self.assertEquals(mdl_fonction.find_by_nom(nom_fonction_plombier).nom_fonction,
                              nom_fonction_plombier)


def create_gestionnaire_par_defaut():
    return PersonneFactory(nom=mdl_personne.NOM_GESTIONNAIRE,
                           prenom=mdl_personne.PRENOM_GESTIONNAIRE)

