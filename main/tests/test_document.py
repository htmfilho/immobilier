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
from main.tests.factories.personne import PersonneFactory
from main.tests.factories.batiment import BatimentFactory
from main.tests.factories.modele_document import ModeleDocumentFactory
from main import document as document_views
from main import models as mdl
from django.core.urlresolvers import reverse


class DocumentViewTest(TestCase):

    def test_no_gestionnaire_detail(self):
        data = {}
        updated_data = document_views._gestionnaire_detail(data)
        self.assertRaises(KeyError, lambda: updated_data[document_views.GESTIONNAIRE_NOM_KEY])
        self.assertRaises(KeyError, lambda: updated_data[document_views.GESTIONNAIRE_PRENOM_KEY])

    def test_gestionnaire_detail(self):
        gestionnaire = PersonneFactory(nom=mdl.personne.NOM_GESTIONNAIRE,
                                       prenom=mdl.personne.PRENOM_GESTIONNAIRE)
        data = {}
        updated_data = document_views._gestionnaire_detail(data)
        self.assertEqual(updated_data[document_views.GESTIONNAIRE_NOM_KEY], mdl.personne.NOM_GESTIONNAIRE)
        self.assertEqual(updated_data[document_views.GESTIONNAIRE_PRENOM_KEY], mdl.personne.PRENOM_GESTIONNAIRE)

    def test_no_batiment_detail(self):
        data = {}
        updated_data = document_views._batiment_detail(None, data)
        self.assertRaises(KeyError, lambda: updated_data[document_views.ADRESSE_KEY])
        self.assertRaises(KeyError, lambda: updated_data[document_views.LOCALITE_KEY])

    def test_batiment_detail(self):
        un_batiment = BatimentFactory()
        data = {}
        updated_data = document_views._batiment_detail(un_batiment, data)
        self.assertEqual(updated_data[document_views.ADRESSE_KEY], un_batiment.adresse_rue)
        self.assertEqual(updated_data[document_views.LOCALITE_KEY], un_batiment.adresse_localite)

    def test_document_bd_list(self):
        ModeleDocumentFactory()
        ModeleDocumentFactory()
        url = reverse('document_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "documents/document_list.html")
        self.assertEqual(len(response.context['documents']), 2)

    def test_document_form(self):
        un_modele = ModeleDocumentFactory()

        url = reverse('document_form', args=[un_modele.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "documents/document_form.html")
        self.assertEqual(response.context['document'], un_modele)
