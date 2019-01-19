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
from django.shortcuts import render, get_object_or_404
from main.forms.forms import BatimentForm
from main import models as mdl
from main import pages_utils
from django.contrib.auth.decorators import login_required
from main.pages_utils import PAGE_LISTE_BATIMENTS


@login_required
def create(request):
    return render(request, pages_utils.PAGE_BATIMENT_FORM,
                  {'batiment':  mdl.batiment.Batiment(),
                   'form': BatimentForm(data=None)})

@login_required
def batiment_form(request, batiment_id):
    batiment = mdl.batiment.find_batiment_by_id(batiment_id)
    return render(request, pages_utils.PAGE_BATIMENT_FORM,
                  {'batiment': batiment,
                   'assurances':   mdl.assurance.find_all(),
                   'localites':    mdl.localite.find_all(),
                   'form': BatimentForm(instance=batiment)})


def _is_updating_action(action):
    if pages_utils.ADD == action or pages_utils.MODIFY == action:
        return True
    return False


def _get_field(field_name, data):
    if data.get(field_name, None) and data.get(field_name, None) != '':
        return data[field_name]
    return None


@login_required
def update(request, batiment_id=None):
    if batiment_id:
        local = get_object_or_404(mdl.batiment.Batiment, pk=batiment_id)
        form = BatimentForm(data=request.POST, instance=local)
    else:
        local = mdl.batiment.Batiment()
        form = BatimentForm(data=request.POST)

    message_info = None

    if request.POST and form.is_valid():
        local = form.save()
        message_info = "Données sauvegardées1"

    return render(request, pages_utils.PAGE_BATIMENT_FORM,
                  {'batiment': local,
                   'message_info': message_info,
                   'form': form})


def _get_localite(request_data):
    if _get_field('localite_cp', request_data) \
            and _get_field('localite_nom', request_data):
        localites_liste = mdl.localite.search(request_data['localite_cp'], request_data['localite_nom'])
        if not localites_liste.exists():
            return mdl.localite.create_localite(request_data['localite_nom'], request_data['localite_cp'])
        else:
            return localites_liste[0]
    return None


def _get_batiment(data):
    if data.get('id') and not data['id'] == 'None':
        return get_object_or_404(mdl.batiment.Batiment, pk=data['id'])
    else:
        return mdl.batiment.Batiment()


@login_required
def search_par_proprietaire(request):
    proprietaire_id = request.GET.get('proprietaire', None)
    batiments = mdl.batiment.search_par_proprietaire(proprietaire_id)
    return render(request, PAGE_LISTE_BATIMENTS,
                  {'batiments': batiments,
                   'proprietaires': mdl.proprietaire.find_distinct_proprietaires()})


def delete(request, batiment_id):
    if batiment_id:
        batiment = get_object_or_404(mdl.batiment.Batiment, pk=batiment_id)
        if batiment:
            batiment.delete()

    return search_par_proprietaire(request)


def donnees_valides(data):
    print(data)
    print(data['localite_nom'])
    print(data['rue'])
    return False
