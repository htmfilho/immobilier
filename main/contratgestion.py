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
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from main.forms.forms import BatimentForm

CONTRATGESTION_LIST_HTML = "contratgestion_list.html"


@login_required
@require_http_methods(["GET", "POST"])
def new(request):
    return render(request, "gestion/create.html",
                  {'action': NEW,
                   'prev': 'fb',
                   'previous': get_previous(request),
                   'form': ContratGestionForm()}
                  )


@login_required
@require_http_methods(["GET", "POST"])
def create(request, batiment_id):
    contrat = None
    batiment = mdl.batiment.find_batiment_by_id(batiment_id)
    if request.POST:
        form = ContratGestionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, pages_utils.PAGE_BATIMENT_FORM, {'batiment': batiment,
                                                                    'form': BatimentForm(instance=batiment)})
    else:
        contrat = mdl.contrat_gestion.ContratGestion()
        contrat.batiment = batiment

        # Par défaut Sté comme gestionnaire
        personne_gestionnaire = mdl.personne.find_gestionnaire_default()
        contrat.gestionnaire = personne_gestionnaire if personne_gestionnaire else None

        form = ContratGestionForm(initial={'batiment': batiment.pk,
                                           'gestionnaire': personne_gestionnaire.id if personne_gestionnaire else None})
    return render(request, "gestion/create.html",
                  {'contrat':   contrat,
                   'action':   NEW,
                   'previous': get_previous(request),
                   'prev':      'fb',
                   'form': form,
                   'batiment': batiment})


@login_required
def prepare_update(request, id_contrat):
    print('prepare_update')
    contrat = mdl.contrat_gestion.find_by_id(id_contrat)
    form = ContratGestionForm(instance=contrat)
    return render(request, "gestion/update.html",
                  {'contrat':   contrat,
                   'action':   UPDATE,
                   'form': form,
                   'previous': get_previous(request),
                   'batiments': mdl.batiment.find_all(),
                   'personnes': [mdl.personne.find_gestionnaire_default()]})


@login_required
@require_http_methods(["GET", "POST"])
def update(request):
    an_id = request.POST.get('id', None)
    return update_contrat_gestion(an_id, request)


def update_contrat_gestion(an_id, request):

    if an_id:
        contrat_de_gestion = mdl.contrat_gestion.find_by_id(an_id)
        form = ContratGestionForm(data=request.POST or None, instance=contrat_de_gestion)

    else:
        form = ContratGestionForm(data=request.POST or None)
        contrat_de_gestion = mdl.contrat_gestion.ContratGestion()
        contrat_de_gestion.batiment = get_object_or_404(mdl.batiment.Batiment,
                                                        pk=request.POST.get('batiment', None))

    if form.is_valid():
        if request.POST.get('action', None) == NEW or request.POST.get('action', None) == UPDATE:
            contrat_de_gestion = form.save()

        return render(request,
                      pages_utils.PAGE_BATIMENT_FORM,
                      {'batiment': contrat_de_gestion.batiment,
                       'contrat_de_gestion': contrat_de_gestion,
                       'form': BatimentForm(instance=contrat_de_gestion.batiment)}
                      )
    else:
        contrat = contrat_de_gestion
        id_contrat = contrat_de_gestion.id
        return render(request, "gestion/update.html", locals())


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
    return render(request, pages_utils.PAGE_BATIMENT_FORM, {'batiment': batiment,
                                                            'form': BatimentForm(instance=batiment)})


@login_required
def saveupdate(request, id_contrat):
    if id_contrat:
        return update_contrat_gestion(id_contrat, request)
    # else:
    #     contrat = mdl.contrat_gestion.find_by_id(id_contrat)
    #     form = ContratGestionForm(instance=contrat)
    #
    #     return render(request, "gestion/update.html",
    #                   {'contrat':   contrat,
    #                    'action':   UPDATE,
    #                    'form': form,
    #                    'previous': get_previous(request),
    #                    'batiments': mdl.batiment.find_all(),
    #                    'personnes': [mdl.personne.find_gestionnaire_default()]})
