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
from django.shortcuts import render, get_object_or_404, redirect
from main.forms import ContratGestionForm
from datetime import datetime
from main.views_utils import get_key
from main import models as mdl


def new(request):
    contrat = mdl.contrat_gestion.ContratGestion()
    personne_gestionnaire = mdl.personne.find_gestionnaire_default()
    if personne_gestionnaire:
        contrat.gestionnaire = personne_gestionnaire
    batiments = mdl.batiment.find_all()
    return render(request, "contratgestion_update.html",
                  {'contrat':   contrat,
                   'personnes': mdl.personne.find_all(),
                   'action':   'new',
                   'prev':      'fb',
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
                   'action':   'new',
                   'batiments': mdl.batiment.find_all(),
                   'prev':      'fb'})


def prepare_update(request, id):

    contrat = mdl.contrat_gestion.find_by_id(id)
    personnes = []
    personne_gestionnaire = mdl.personne.find_gestionnaire_default()
    personnes.append(personne_gestionnaire)
    return render(request, "contratgestion_update.html",
                  {'contrat':   contrat,
                   'action':   'update',
                   'personnes': personnes})


def update(request):
    """
    ok - 1
    """
    print('update CONTRAT  GESTION')
    previous = request.POST.get('previous', None)
    form = ContratGestionForm(data=request.POST)
    gestion = None
    personne = None

    print(form['batiment_id'].value())

    batiment_id = mdl.batiment.Batiment(form['batiment_id'].value()).id
    # batiment_id = get_key(request.POST.get('batiment_id', None))
    print('action : ', request.POST.get('action', None))
    if request.POST.get('action', None) == 'new':
        gestion = mdl.contrat_gestion.ContratGestion()
        batiment = get_object_or_404(mdl.batiment.Batiment, pk=batiment_id)
        gestion.batiment = batiment
    else:
        if request.POST.get('id', None) != '':
            gestion = get_object_or_404(mdl.contrat_gestion.ContratGestion, pk=request.POST.get('id', None))
            batiment = get_object_or_404(mdl.batiment.Batiment, pk=batiment_id)
            gestion.batiment = batiment
    if gestion is None:
        gestion = mdl.contrat_gestion.ContratGestion()
        batiment = get_object_or_404(mdl.batiment.Batiment, pk=batiment_id)
        gestion.batiment = batiment
    if request.POST.get('gestionnaire', None):
        personne = get_object_or_404(mdl.personne.Personne, pk=request.POST.get('gestionnaire', None))
        gestion.gestionnaire = personne
    if request.POST.get('montant_mensuel', None):
        gestion.montant_mensuel = request.POST.get('montant_mensuel')
    if request.POST.get('date_debut', None):
        try:
            valid_datetime = datetime.strptime(request.POST['date_debut'], '%d/%m/%Y')
            gestion.date_debut = valid_datetime
        except:
            gestion.date_debut = None
    else:
        gestion.date_debut = None

    # gestion.date_fin = request.POST['date_fin']
    if request.POST.get('date_fin', None):
        try:
            valid_datetime = datetime.strptime(request.POST['date_fin'], '%d/%m/%Y')
            gestion.date_fin = valid_datetime
        except:
            gestion.date_fin = None
    else:
        gestion.date_fin = None
    if gestion.date_debut and gestion.date_fin:
        if gestion.date_debut > gestion.date_fin:
            return render(request, "contratgestion_update.html",
                          {'contrat': gestion,
                           'message': 'La date de début doit être < à la date de fin'})
    if personne is None:
        print('personne is none')
        message = "Il faut sélectionner un gestionnaire"
        return render(request, "contratgestion_update.html",
                      {'contrat': gestion,
                       'action':   'update',
                       'message': message,
                       'form':     form})
    if form.is_valid() and data_valid(form, gestion):
        print('form valid')
        montant_mensuel = request.POST.get('montant_mensuel', None)
        if montant_mensuel:
            try:
                gestion.montant_mensuel = float(montant_mensuel.replace(',', '.'))
            except:
                gestion.montant_mensuel = None
        gestion.save()
        return redirect(previous)
    else:
        print('form invalid')
        personnes = []
        personne_gestionnaire = mdl.personne.find_gestionnaire_default()
        personnes.append(personne_gestionnaire)
        return render(request, "contratgestion_update.html",
                      {'contrat': gestion,
                       'action': 'update',
                       'message': 'Invalide',
                       'form': form,
                       'personnes': personnes,
                       'batiments': mdl.batiment.find_all()})
        # return render_to_response("contratgestion_update.html",
        #                           {'contrat': gestion,
        #                            'action': 'update',
        #                            'message': 'Invalide',
        #                            'form': form,
        #                            'personnes': personnes,
        #                            'batiments': mdl.batiment.objects.all()}, context_instance=RequestContext(request))


def list(request):
    contrats = mdl.contrat_gestion.find_all()
    return render(request, "contratgestion_list.html",
                           {'contrats': contrats})


def delete(request, contrat_gestion_id):
    contrat_gestion = get_object_or_404(mdl.contrat_gestion.ContratGestion, pk=contrat_gestion_id)
    batiment = contrat_gestion.batiment
    if contrat_gestion:
        contrat_gestion.delete()
    return render(request, "batiment_form.html", {'batiment': batiment})


def data_valid(form, contrat):
    # contrat = ContratGestion.search(contrat.batiment, contrat.date_debut, contrat.date_fin)
    # if contrat.exists():
    #
    #     return False
    return True
