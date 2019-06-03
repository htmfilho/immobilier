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
from main.forms.forms import  FraisMaintenanceForm
from main.views_utils import get_key, get_date
from main import models as mdl
from main import pages_utils
from main.pages_utils import NEW, UPDATE, PAGE_FRAIS_FORM
from main.views_utils import get_previous
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from main import societe
from django.contrib.auth.decorators import login_required
from main.forms.forms import BatimentForm

ON = 'on'

FRAIS_LIST_HTML = "frais/fraismaintenance_list.html"

LISTE = 'liste'
DASHBOARD = 'dashboard'
LOCATION = 'location'
BATIMENT = 'batiment'


@login_required
def new(request):
    frais = mdl.frais_maintenance.FraisMaintenance()
    return render(request, PAGE_FRAIS_FORM,
                  {'frais':     frais,
                   'personnes': mdl.personne.find_all(),
                   'action':   NEW,
                   'batiments': mdl.batiment.find_all(),
                   'contrats_location': mdl.contrat_location.find_all(),
                   'entrepreneurs': mdl.professionnel.find_all(),
                   'societes': mdl.societe.find_all_with_name(),
                   'fonctions': mdl.fonction.find_all(),
                   'previous':  get_previous(request)})


@login_required
def create(request, batiment_id):
    batiment = get_object_or_404(mdl.batiment.Batiment, pk=batiment_id)
    frais = mdl.frais_maintenance.FraisMaintenance()
    frais.batiment = batiment
    previous = 'batiment'
    return render(request, PAGE_FRAIS_FORM,
                  {'frais':     frais,
                   'personnes': mdl.personne.find_all(),
                   'action':   NEW,
                   'batiments': mdl.batiment.find_all(),
                   'entrepreneurs': mdl.professionnel.find_all(),
                   'societes': mdl.societe.find_all_with_name(),
                   'fonctions': mdl.fonction.find_all(),
                   'previous':  previous
                   })


@login_required
def prepare_update(request, frais_id, previous=None, location_id=None):
    frais = mdl.frais_maintenance.find_by_id(frais_id)

    return render(request, PAGE_FRAIS_FORM,
                  {'frais':  frais,
                   'action': UPDATE,
                   'entrepreneurs': mdl.professionnel.find_all(),
                   'location_id': location_id,
                   'previous': previous})


@login_required
def update(request):
    batiment_id = get_key(request.POST.get('batiment_id', None))
    action = request.POST.get('action', None)

    frais = _populate_frais(action, batiment_id, request)
    contrat_location_id = get_contrat_location_id(frais, request.POST.get('location_id', None), request.POST.get('contrat_location'))

    form = FraisMaintenanceForm(data=request.POST)
    previous = request.POST.get('previous', None)
    if form.is_valid():
        frais.save()
        return redirection_to_previous(batiment_id, contrat_location_id, previous)
    else:
        return render(request, PAGE_FRAIS_FORM, {
            'frais': frais,
            'form': form,
            'action': action,
            'previous': previous,
            'entrepreneurs': mdl.professionnel.find_all(),
            'societes': mdl.societe.find_all_with_name(),
            'fonctions': mdl.fonction.find_all()})


def redirection_to_previous(batiment_id, contrat_location_id, previous):
    if previous == 'batiment':
        return HttpResponseRedirect(reverse('batiment', args=(batiment_id,)))
    elif previous == 'location' and contrat_location_id:
        return HttpResponseRedirect(reverse('location-prepare-update-all', args=(contrat_location_id,)))
    elif previous == 'dashboard':
        return redirect('home')
    elif previous == 'liste':
        return HttpResponseRedirect(reverse('fraismaintenance_list'))
    else:
        return ''


def _populate_frais(action, batiment_id, request):
    frais = set_batiment(action, batiment_id, request.POST.get('id', None))
    frais.contrat_location = None
    frais.entrepreneur = _get_professionnel(request.POST)
    frais.description = request.POST.get('description', None)
    frais.montant = get_montant(request)
    frais.date_realisation = get_date(request.POST.get('date_realisation', None))
    return frais


def get_montant(request):
    if request.POST.get('montant', None):
        try:
            montant = float(request.POST['montant'].replace(',', '.'))
        except:
            montant = 0
    else:
        montant = 0
    return montant


def _get_professionnel(request_data):
    professionnel = None
    if request_data.get('new_entrepreneur') == ON:
        professionnel = nouveau_professionnel(request)
    else:
        entrepreneur = get_key(request_data.get('entrepreneur', None))
        if entrepreneur:
            professionnel = get_object_or_404(mdl.professionnel.Professionnel, pk=entrepreneur)
    return professionnel


def get_contrat_location_id(frais, location_id, contrat_location_check_box):
    contrat_location_id = location_id
    if contrat_location_check_box == ON:
        contrat_de_location_actuel = frais.batiment.location_actuelle
        if contrat_de_location_actuel:
            frais.contrat_location = contrat_de_location_actuel
            contrat_location_id = contrat_de_location_actuel.id
    return contrat_location_id


def set_batiment(action, batiment_id, frais_id):
    frais = None
    if action == NEW:
        frais = mdl.frais_maintenance.FraisMaintenance()
        if batiment_id:
            batiment = get_object_or_404(mdl.batiment.Batiment, pk=batiment_id)
            frais.batiment = batiment
    else:
        if frais_id:
            frais = get_object_or_404(mdl.frais_maintenance.FraisMaintenance, pk=frais_id)
        if batiment_id:
            frais.batiment = get_object_or_404(mdl.batiment.Batiment, pk=batiment_id)
        else:
            frais.batiment = None
    return frais


def nouveau_professionnel(request_data):
    # nouvel entrepreneur
    professionnel = mdl.professionnel.Professionnel(personne=get_personne(request_data),
                                                    societe=get_societe(request_data),
                                                    fonction=get_fonction(request_data))
    professionnel.save()
    return professionnel


def get_fonction(request_data):
    if is_new_value(request_data.get('new_fonction', None)):
        new_value = request_data.get('new_fonction', None)
        if new_value:
            return creation_nouvelle_fonction(new_value)
    else:
        return get_object_or_404(mdl.fonction.Fonction, pk=get_key(request_data.get('new_fonction', None)))
    return None


def creation_nouvelle_fonction(new_value):
    fonction = mdl.fonction.Fonction(nom_fonction=new_value)
    fonction.save()
    return fonction


def get_societe(request_data):
    if is_new_value(request_data.get('new_societe', None)):
        new_value = request_data.get('new_societe', None)
        if new_value:
            return societe.creation_nouvelle_societe(new_value)
    else:
        societe_id = get_key(request_data.get('new_societe', None))
        return get_object_or_404(mdl.societe.Societe, pk=societe_id)
    return None


def get_personne(request_data):
    if is_new_value(request_data.get('new_personne', None)):
        return create_new_personne(request_data.get('new_personne', None))
    else:
        personne_id = get_key(request_data.get('new_personne', None))
        return get_object_or_404(mdl.personne.Personne, pk=personne_id)


def create_new_personne(concatenation_nom_prenom):
    if concatenation_nom_prenom:
        nom_prenom = get_tableau_nom_prenom(concatenation_nom_prenom)
        return mdl.personne.creation_nouvelle_personne(nom_prenom[0], nom_prenom[1])
    return None


def get_tableau_nom_prenom(personne_new_value):
    nom_prenom = personne_new_value.split(' ')
    if len(nom_prenom) >= 2:
        return nom_prenom
    return None


def list(request):
    frais_list = mdl.frais_maintenance.find_all()
    return render(request, FRAIS_LIST_HTML,
                  {'frais_list': frais_list})


def delete(request, id, previous):
    frais = get_object_or_404(mdl.frais_maintenance.FraisMaintenance, pk=id)
    if frais:
        frais.delete()
    return render(request, "fraismaintenance_confirm_delete.html",
                           {'object': frais, 'previous': previous})


def contrat_new(request, contrat_location_id):
    frais = mdl.frais_maintenance.FraisMaintenance()
    # previous = request.POST.get('previous', None)
    previous = "location"
    location = get_object_or_404(mdl.contrat_location.ContratLocation, pk=contrat_location_id)
    if location:
        frais.contrat_location = location
        frais.batiment = location.batiment
    return render(request, PAGE_FRAIS_FORM,
                  {'frais':             frais,
                   'location_id': contrat_location_id,
                   'personnes':         mdl.personne.find_all(),
                   'action':            NEW,
                   'batiments':         mdl.batiment.find_all(),
                   'contrats_location': mdl.contrat_location.find_all(),
                   'entrepreneurs':     mdl.professionnel.find_all(),
                   'previous':          previous})


def is_new_value(id):
    if id is None or id == "" or id == "-" or id == "None":
        id = None
    if id:
        try:
            int(id)
            return False
        except:
            return True


def delete_frais(request, id, previous):
    frais = mdl.frais_maintenance.find_by_id(id)
    batiment = frais.batiment
    contrat_location = frais.contrat_location
    if frais:
        frais.delete()

    return get_redirection(batiment, contrat_location, previous, request)


def get_redirection(batiment, contrat_location, previous, request):
    if previous == 'batiment':
        return HttpResponseRedirect(reverse('batiment', args=(batiment.id,)))
    if previous == 'location':
        return HttpResponseRedirect(reverse('location-prepare-update-all', args=(contrat_location.id,)))
    if previous == 'liste':
        return HttpResponseRedirect(reverse('fraismaintenance_list'))
    return render(request, pages_utils.PAGE_BATIMENT_FORM, {'batiment': batiment,
                                                            'form': BatimentForm(instance=batiment)})


def prepare_update_from_batiment(request, id):
    return prepare_update(request, id, BATIMENT, None)


def prepare_update_from_location(request, id):
    location_id = request.POST.get('id', None)
    return prepare_update(request, id, LOCATION, location_id)


def prepare_update_from_dashboard(request, id):
    return prepare_update(request, id, DASHBOARD, None)


def prepare_update_from_list(request, id):
    return prepare_update(request, id, LISTE, None)


def delete_frais_from_batiment(request, id):
    return delete_frais(request, id, BATIMENT)


def delete_frais_from_location(request, id):
    return delete_frais(request, id, LOCATION)


def delete_frais_from_list(request, id):
    return delete_frais(request, id, LISTE)
