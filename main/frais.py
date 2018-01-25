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
from main.forms import FraisMaintenanceForm
from main.views_utils import get_key, get_date
from main import models as mdl
from main import pages_utils
from main.pages_utils import NEW, UPDATE, PAGE_FRAIS_FORM
from main.views_utils import get_previous
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from main import societe


FRAIS_LIST_HTML = "frais/fraismaintenance_list.html"

LISTE = 'liste'
DASHBOARD = 'dashboard'
LOCATION = 'location'
BATIMENT = 'batiment'


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


def prepare_update(request, frais_id, previous=None, location_id=None):
    frais = mdl.frais_maintenance.find_by_id(frais_id)

    return render(request, PAGE_FRAIS_FORM,
                  {'frais':  frais,
                   'action': UPDATE,
                   'entrepreneurs': mdl.professionnel.find_all(),
                   'location_id': location_id,
                   'previous': previous})


def update(request):
    print('update')
    location_id = request.POST.get('location_id', None)
    batiment_id = get_key(request.POST.get('batiment_id', None))
    action = request.POST.get('action', None)

    frais = set_batiment(action, batiment_id, request.POST.get('id', None))
    frais.contrat_location = None
    contrat_location_id = get_contrat_location_id(frais, location_id, request)
    frais.entrepreneur = get_professionnel(request)
    frais.description = request.POST.get('description', None)
    frais.montant = get_montant(request)
    frais.date_realisation = get_date(request.POST.get('date_realisation', None))

    form = FraisMaintenanceForm(data=request.POST)
    previous = request.POST.get('previous', None)
    if form.is_valid():
        print('previous {}'.format(previous))
        frais.save()

        if previous == 'batiment':
            return HttpResponseRedirect(reverse('batiment', args=(batiment_id, )))
        if previous == 'location' and contrat_location_id:
            return HttpResponseRedirect(reverse('location-prepare-update-all', args=(contrat_location_id, )))
        if previous == 'dashboard':
            return redirect('home')
        if previous == 'liste':
            return HttpResponseRedirect(reverse('fraismaintenance_list'))

    else:

        previous = request.POST.get('previous', None)
        return render(request, PAGE_FRAIS_FORM, {
            'frais': frais,
            'form': form,
            'action': action,
            'previous': previous,
            'entrepreneurs': mdl.professionnel.find_all(),
            'societes': mdl.societe.find_all_with_name(),
            'fonctions': mdl.fonction.find_all()})


def get_montant(request):
    if request.POST.get('montant', None):
        try:
            montant = float(request.POST['montant'].replace(',', '.'))
        except:
            montant = 0
    else:
        montant = 0
    return montant


def get_professionnel(request):
    professionnel = None
    if request.POST.get('new_entrepreneur') == 'on':
        professionnel = nouveau_professionnel(request)
    else:
        entrepreneur = get_key(request.POST.get('entrepreneur', None))
        if entrepreneur:
            professionnel = get_object_or_404(mdl.professionnel.Professionnel, pk=entrepreneur)
    return professionnel


def get_contrat_location_id(frais, location_id, request):
    contrat_location_id = location_id
    if request.POST.get('contrat_location') == 'on':
        cl = frais.batiment.location_actuelle
        if cl:
            frais.contrat_location = cl
            contrat_location_id = cl.id
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


def nouveau_professionnel(request):
    # nouvel entrepreneur
    personne = get_personne(request)
    societe = get_societe(request)
    fonction = get_fonction(request)
    professionnel = mdl.professionnel.Professionnel(personne=personne,
                                                    societe=societe,
                                                    fonction=fonction)
    professionnel.save()
    return professionnel


def get_fonction(request):
    if is_new_value(request.POST.get('new_fonction', None)):
        new_value = request.POST.get('new_fonction', None)
        if new_value:
            return creation_nouvelle_fonction(new_value)
    else:
        return get_object_or_404(mdl.fonction.Fonction, pk=get_key(request.POST.get('new_fonction', None)))
    return None


def creation_nouvelle_fonction(new_value):
    fonction = mdl.fonction.Fonction(nom_fonction=new_value)
    fonction.save()
    return fonction


def get_societe(request):
    if is_new_value(request.POST.get('new_societe', None)):
        new_value = request.POST.get('new_societe', None)
        if new_value:
            return societe.creation_nouvelle_societe(new_value)
    else:
        societe_id = get_key(request.POST.get('new_societe', None))
        return get_object_or_404(mdl.societe.Societe, pk=societe_id)
    return None


def get_personne(request):
    if is_new_value(request.POST.get('new_personne', None)):
        personne_new_value = request.POST.get('new_personne', None)

        if personne_new_value:
            nom_prenom = personne_new_value.split(' ')
            if len(nom_prenom) >= 2:
                personne = mdl.personne.Personne()
                personne.nom = nom_prenom[0]
                personne.prenom = nom_prenom[1]
                personne.save()
                return personne
    else:
        personne_id = get_key(request.POST.get('new_personne', None))
        return get_object_or_404(mdl.personne.Personne, pk=personne_id)
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
    print('contrat_new')
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
    return render(request, pages_utils.PAGE_BATIMENT_FORM, {'batiment': batiment})


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
