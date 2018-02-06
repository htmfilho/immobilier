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
from main.forms import ContratGestionForm
from main import models as mdl
from main import pages_utils
from main.pages_utils import NEW, UPDATE
from main.views_utils import get_previous
from main.views_utils import get_date


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


def create(request, batiment_id):
    """
    ok - 1
    """
    batiment = mdl.batiment.find_batiment(batiment_id)
    contrat = mdl.contrat_gestion.ContratGestion()
    contrat.batiment = batiment
    # Par défaut Sté comme gestionnaire

    personne_gestionnaire = mdl.personne.find_gestionnaire_default()
    if personne_gestionnaire:
        contrat.gestionnaire = personne_gestionnaire

    return render(request, "contratgestion_update.html",
                  {'contrat':   contrat,
                   'personnes': mdl.personne.find_all(),
                   'action':   NEW,
                   'batiments': mdl.batiment.find_all(),
                   'previous': get_previous(request),
                   'prev':      'fb'})


def prepare_update(request, id):
    contrat = mdl.contrat_gestion.find_by_id(id)
    personne_gestionnaire = mdl.personne.find_gestionnaire_default()
    personnes = [personne_gestionnaire]
    return render(request, "contratgestion_update.html",
                  {'contrat':   contrat,
                   'action':   UPDATE,
                   'previous': get_previous(request),
                   'batiments': mdl.batiment.find_all(),
                   'personnes': personnes})


def update(request):
    previous = request.POST.get('previous', None)
    form = ContratGestionForm(data=request.POST)
    gestion = None
    personne = None

    batiment_id = mdl.batiment.Batiment(form['batiment_id'].value()).id
    if batiment_id == '-':
        batiment_id = None

    # batiment_id = get_key(request.POST.get('batiment_id', None))
    if request.POST.get('action', None) == NEW:
        gestion = mdl.contrat_gestion.ContratGestion()
        batiment = get_object_or_404(mdl.batiment.Batiment, pk=batiment_id)
        gestion.batiment = batiment
    else:
        if request.POST.get('id', None) != '':
            gestion = get_object_or_404(mdl.contrat_gestion.ContratGestion, pk=request.POST.get('id', None))
            batiment = get_object_or_404(mdl.batiment.Batiment, pk=batiment_id)
            gestion.batiment = batiment
    gestion = get_contrat_gestion(batiment_id, gestion)
    if request.POST.get('gestionnaire', None):
        personne = get_object_or_404(mdl.personne.Personne, pk=request.POST.get('gestionnaire', None))
        gestion.gestionnaire = personne
    if request.POST.get('montant_mensuel', None):
        gestion.montant_mensuel = request.POST.get('montant_mensuel')

    gestion.date_debut = get_date(request.POST.get('date_debut', None))
    gestion.date_fin = get_date(request.POST.get('date_fin', None))

    if personne is None:
        message = "Il faut sélectionner un gestionnaire"
        return render(request, "contratgestion_update.html",
                      {'contrat': gestion,
                       'action':  UPDATE,
                       'message': message,
                       'form':    form})
    if form.is_valid() and data_valid(form, gestion):
        gestion.montant_mensuel = get_montant(request.POST.get('montant_mensuel', None))
        gestion.save()
        return redirect(previous)
    else:
        return render(request, "contratgestion_update.html",
                      {'contrat':   gestion,
                       'action':    UPDATE,
                       'message':   'Invalide',
                       'form':      form,
                       'personnes': [mdl.personne.find_gestionnaire_default()],
                       'batiments': mdl.batiment.find_all(),
                       'previous': previous})


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
