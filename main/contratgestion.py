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
from django.shortcuts import render, get_object_or_404, redirect
from main.forms.contrat_gestion import ContratGestionForm
from main import models as mdl
from main import pages_utils
from main.pages_utils import NEW, UPDATE
from main.views_utils import get_previous
from main.views_utils import get_date
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponseRedirect
from django.urls import reverse

CONTRATGESTION_LIST_HTML = "contratgestion_list.html"


def new(request):
    contrat = mdl.contrat_gestion.ContratGestion()
    personne_gestionnaire = mdl.personne.find_gestionnaire_default()
    if personne_gestionnaire:
        contrat.gestionnaire = personne_gestionnaire
    batiments = mdl.batiment.find_all()
    return render(request, "contratgestion_update.html",
                  {'contrat':   contrat,
                   'personnes': mdl.personne.find_all(),
                   'action':   NEW,
                   'prev':      'fb',
                   'previous': get_previous(request),
                   'batiments': batiments})

@login_required
@require_GET
def create(request, batiment_id):
    print('create')
    batiment = mdl.batiment.find_batiment_by_id(batiment_id)
    contrat = mdl.contrat_gestion.ContratGestion()
    contrat.batiment = batiment
    # Par défaut Sté comme gestionnaire
    personne_gestionnaire = mdl.personne.find_gestionnaire_default()
    if personne_gestionnaire:
        contrat.gestionnaire = personne_gestionnaire
    print('create {}'.format(contrat))
    # form = ContratGestionForm(None, instance=contrat, batiment=batiment)
    form = ContratGestionForm(initial={'batiment': batiment.pk, 'gestionnaire': personne_gestionnaire.id})

    return render(request, "gestion/create.html",
                  {'contrat':   contrat,
                   'personnes': mdl.personne.find_all(),
                   'action':   NEW,
                   'batiments': mdl.batiment.find_all(),
                   'previous': get_previous(request),
                   'prev':      'fb',
                   'form': form,
                   'batiment': batiment})

@login_required
def prepare_update(request, id_contrat):
    print('prepare_update')
    contrat = mdl.contrat_gestion.find_by_id(id)
    form = ContratGestionForm(instance=contrat)
    personne_gestionnaire = mdl.personne.find_gestionnaire_default()
    personnes = [personne_gestionnaire]
    return render(request, "gestion/update.html",
                  {'contrat':   contrat,
                   'action':   UPDATE,
                   'form': form,
                   'previous': get_previous(request),
                   'batiments': mdl.batiment.find_all(),
                   'personnes': personnes})

@login_required
@require_POST
def update(request):
    print('update')
    previous = request.POST.get('previous', None)
    an_id =  request.POST.get('id', None)
    print(an_id)
    if an_id:
        form = ContratGestionForm(data = request.POST or None, instance=mdl.contrat_gestion.find_by_id(an_id))
    else:
        form = ContratGestionForm(data = request.POST or None)
    gestion = None
    personne = None
    batiment_id = None

    if form.is_valid():
        print('is_valid')
        if request.POST.get('action', None) == NEW or request.POST.get('action', None) == UPDATE:
            gestion = form.save(commit=True)
        return render(request, pages_utils.PAGE_BATIMENT_FORM, {'batiment': gestion.batiment})
    else:
        print('is_invalid')
        # return HttpResponseRedirect(reverse('gestion-prepare-update-all', args=(an_id,)))
        return render(request, "contratgestion_update.html",
                      {'id': an_id,
                       'action':    UPDATE,
                       'form':      form,

                       'previous': previous})
    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})


def get_contrat_gestion(batiment_id, gestion):
    if gestion is None:
        gestion = mdl.contrat_gestion.ContratGestion()
        batiment = get_object_or_404(mdl.batiment.Batiment, pk=batiment_id)
        gestion.batiment = batiment
    return gestion


def get_montant(montant_mensuel):
    if montant_mensuel:
        try:
            return float(montant_mensuel.replace(',', '.'))
        except:
            return None
    return None


def list(request):
    contrats = mdl.contrat_gestion.find_all()
    return render(request, CONTRATGESTION_LIST_HTML,
                  {'contrats': contrats})


def delete(request, contrat_gestion_id):
    contrat_gestion = get_object_or_404(mdl.contrat_gestion.ContratGestion, pk=contrat_gestion_id)
    batiment = None
    if contrat_gestion:
        batiment = contrat_gestion.batiment
        contrat_gestion.delete()
    return render(request, pages_utils.PAGE_BATIMENT_FORM, {'batiment': batiment})


def data_valid(form, contrat):
    # contrat = ContratGestion.search(contrat.batiment, contrat.date_debut, contrat.date_fin)
    # if contrat.exists():
    #
    #     return False
    return True
