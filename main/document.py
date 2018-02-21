#############################################################################
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
from main import models as mdl
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import *
from main.forms.forms import  LettreForm, LigneForm

from templated_docs import fill_template
from templated_docs.http import FileResponse
from django.forms import formset_factory
import re

DEFAULT_CIVILITE_ = 'Madame, Monsieur,'

PRENOM_KEY = 'prenom'
NOM_KEY = 'nom'
ADRESSE_KEY = 'adresse'
LOCALITE_KEY = 'localite'
GESTIONNAIRE_NOM_KEY = 'gestionnaire_nom'
GESTIONNAIRE_PRENOM_KEY = 'gestionnaire_prenom'


def document_bd_list(request):
    return render(request, "documents/document_list.html",
                  {'documents': mdl.modele_document.find_all()})


def document_form(request, document_id):
    return render(request, "documents/document_form.html",
                  {'document': mdl.modele_document.find_by_id(document_id)})


def lettre_indexation_form(request, contrat_location_id):
    modele = mdl.modele_document.find_by_reference('LETTRE_INDEXATION')
    form = None
    formset = None
    contrat_location = None
    if request.method == 'POST':
        pass
    else:
        if contrat_location_id:
            contrat_location = mdl.contrat_location.find_by_id(contrat_location_id)

        ArticleFormSet = formset_factory(LigneForm, extra=2)
        formset = None
        # formset = ArticleFormSet(initial=[{'test': 'Django is now open source', },
        #                                   {'test': 'Django is now open source2', }])
        #
        form = LettreForm(initial={'sujet': modele.sujet,
                                   'format': "docx",
                                   'fichier_modele': modele.fichier_modele,
                                   'titre': 'Monsieur',
                                   'tableSet': formset})
    # form = LettreForm(request.POST or None)
    return render(request, "documents/lettre.html", {'form': form,
                                                     'formset': formset,
                                                     'contrat_location': contrat_location,
                                                     'modele':  modele})


def lettre_indexation(request, contrat_location_id):
    modele = mdl.modele_document.find_by_reference('LETTRE_INDEXATION')
    a_contrat_location = mdl.contrat_location.find_by_id(contrat_location_id)

    doctype = request.POST.get('format_fichier', 'pdf')

    ArticleFormSet = formset_factory(LigneForm, extra=2)
    formset = ArticleFormSet(initial=[{'test': 'Django is now open source', },
                                      {'test': 'Django is now open source2', }])
    data = _build_data(formset)

    locataires = a_contrat_location.locataires
    locataire = locataires.first()

    if locataire:
        personne = locataire.personne
        data.update({'titre': _get_civilite(locataire.civilite)})
        if personne:
            data.update({NOM_KEY: personne.nom})
            data.update({PRENOM_KEY: personne.prenom})

    data.update({"sujet": "Lettre d'indexation"})

    data = _batiment_detail(a_contrat_location.batiment, data)
    data = _gestionnaire_detail(data)

    filename = fill_template(
        "documents/{}".format(modele.fichier_modele), data,
        output_format=doctype)
    return FileResponse(filename, 'LETTRE_INDEXATION.{}'.format(doctype))


def _gestionnaire_detail(data_param):
    data = data_param
    personne_gestionnaire = mdl.personne.find_gestionnaire_default()
    if personne_gestionnaire:
        data.update({GESTIONNAIRE_NOM_KEY: personne_gestionnaire.nom})
        data.update({GESTIONNAIRE_PRENOM_KEY: personne_gestionnaire.prenom})
    return data


def _batiment_detail(un_batiment, data_param):
    data = data_param
    if un_batiment:
        data.update({ADRESSE_KEY: un_batiment.adresse_rue})
        data.update({LOCALITE_KEY: un_batiment.adresse_localite})
    return data


def _build_data(formset):
    data = {}
    ligne_test = LigneTest()
    ligne_test.col1 = 'col1'
    ligne_test.col2 = 'col2'
    ligne_test_2 = LigneTest()
    ligne_test_2.col1 = 'col12'
    ligne_test_2.col2 = 'col22'
    data.update({'lignes': [ligne_test, ligne_test_2]})
    data.update({'l1': 'l1'})
    data.update({'l2': 'l2'})
    data.update({'html': '<table><tr><td>sss</td><td>ksdf</td></tr></table>'})
    data.update({'formset': formset})
    data.update({'dateJour': timezone.now()})
    return data


class LigneTest:
    def __init__(self):
        self.col1 = "Ferrari"
        self.col2 = "Ferrari"

    def ligne_complete(self):
        return "{0} {1}".format(self.col1, self.col2)


def lettre_indexation_new(request, contrat_location_id):
    document_modele = mdl.document_modele.find_by_reference('LETTRE_INDEXATION')
    if document_modele:
        return create_document(contrat_location_id, document_modele, request)


def create_document(contrat_location_id, document_modele, request):
    variables = {}
    input = document_modele.contenu
    ll = re.findall(r"\[([^\]]*)\]*", input)
    un_contrat_location = mdl.contrat_location.find_by_id(contrat_location_id)
    if un_contrat_location and un_contrat_location.batiment:
        batiment = un_contrat_location.batiment
        variables.update({'batiment_description': batiment.description,
                          'batiment_rue': batiment.rue,
                          'batiment_numero': batiment.numero,
                          'batiment_boite': batiment.boite,
                          'batiment_lieu_dit': batiment.lieu_dit,
                          'batiment_localite': batiment.localite,
                          'batiment_superficie': batiment.superficie,
                          'batiment_performance_energetique': batiment.performance_energetique})
    for key in ll:
        value = ''
        if key not in variables:
            variables.update({'{}'.format(key): value})
        else:
            input = input.replace(key, 'kkk')
    return render(request, 'documents/document.html', {'document': document_modele,
                                                       'contenu': input,
                                                       'variables': variables})


def _get_civilite(civilite):
    if civilite:
        return civilite.capitalize()
    return DEFAULT_CIVILITE_
