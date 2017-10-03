#############################################################################
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
from main import models as mdl
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import *
from main.forms import LettreForm, \
    LigneForm

from templated_docs import fill_template
from templated_docs.http import FileResponse
from django.forms import formset_factory


def lettre_create(request):
    print('lettre_create')
    formset = None
    if request.method == 'POST':
        form = LettreForm(request.POST or None)
        formset = LigneForm(request.POST or None)
        ArticleFormSet = formset_factory(LigneForm, extra=2)
        formset = ArticleFormSet(initial=[{'test': 'Django is now open source', },
                                          {'test': 'Django is now open source2', }])
    else:
        form = LettreForm()

    if form.is_valid():
        doctype = 'docx'
        data = form.cleaned_data
        location = data['location']

        # lignes = []
        # ligne1 = LigneTest()
        # ligne1.col1 = "col1"
        # ligne1.col2 = "col2"
        #
        # ligne2 = LigneTest()
        # ligne2.col1 = "col12"
        # ligne2.col2 = "col22"
        #
        # lignes.append(ligne1)
        # lignes.append(ligne2)
        #
        # data.update({'lignes': lignes})
        # data.update({'l1': 'l1'})
        # data.update({'l2': 'l2'})
        # data.update({'html': '<table><tr><td>sss</td><td>ksdf</td></tr></table>'})
        #
        # ArticleFormSet = formset_factory(LigneForm, extra=2)
        # formset = ArticleFormSet(initial=[{'test': 'Django is now open source', },
        #                                   {'test': 'Django is now open source2', }])
        # data.update({'formset': formset})

        data.update({'dateJour': timezone.now()})
        # personne = mdl.personne.find_personne(1)
        locataires = location.locataires
        personne = None
        if locataires:
            personne = location.locataires.first().personne
        if personne:
            data.update({'titre': personne.titre})
            data.update({'nom': personne.nom})
            data.update({'prenom': personne.prenom})
        bat = mdl.batiment.find_batiment(1)
        bat = location.batiment
        data.update({'adresse': bat.adresse_rue})
        data.update({'localite': bat.adresse_localite})
        personne_gestionnaire = mdl.personne.find_gestionnaire_default()
        data.update({'gestionnaire_nom': personne_gestionnaire.nom})
        data.update({'gestionnaire_prenom': personne_gestionnaire.prenom})
        data.update({'tableau': [['ligne1','ligne2'],['ligne1','ligne2']]})

        filename = fill_template(
            'documents/lettre.odt', data,
            output_format=doctype)
        visible_filename = 'lettre.{}'.format(doctype)

        return FileResponse(filename, visible_filename)
    else:
        return render(request, 'documents/lettre.html', {'form': form})


class LigneTest:

    def __init__(self):
        self.col1 = "Ferrari"
        self.col2 = "Ferrari"

    def ligne_complete(self):
        return "{0} {1}".format(self.col1, self.col2)
