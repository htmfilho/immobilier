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
from datetime import datetime
from main.forms import FraisMaintenanceForm
from main.views_utils import get_key
from main import models as mdl
from main import pages_utils
from main.pages_utils import NEW, UPDATE, PAGE_FRAIS_FORM
from main.views_utils import get_previous
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

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
    previous = request.META.get('HTTP_REFERER', '/')
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


def prepare_update(request, id, previous):
    print('prepare_update')
    print(previous)
    frais = mdl.frais_maintenance.find_by_id(id)

    return render(request, PAGE_FRAIS_FORM,
                  {'frais':  frais,
                   'action': UPDATE,
                   'entrepreneurs': mdl.professionnel.find_all(),
                   'previous': previous})


def update(request):
    batiment_id = get_key(request.POST.get('batiment_id', None))
    action = request.POST.get('action', None)
    frais_id = request.POST.get('id', None)

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
    frais.contrat_location = None
    if request.POST.get('contrat_location') == 'on':
        cl = frais.batiment.location_actuelle
        if cl:
            frais.contrat_location = cl

    professionnel = None
    if request.POST.get('new_entrepreneur') == 'on':
        professionnel = nouveau_professionnel(request)
    else:
        entrepreneur = get_key(request.POST.get('entrepreneur', None))
        if entrepreneur:
            professionnel = get_object_or_404(mdl.professionnel.Professionnel, pk=entrepreneur)

    frais.entrepreneur = professionnel
    # if request.POST.get('societe', None):
    #     frais.societe = request.POST['societe']
    # else:
    #     frais.societe = None
    if request.POST.get('description', None):
        frais.description = request.POST['description']
    else:
        frais.description = None

    if request.POST.get('montant', None):
        try:
            frais.montant = float(request.POST['montant'].replace(',', '.'))
        except:
            frais.montant = 0
    else:
        frais.montant = 0
    if request.POST.get('date_realisation', None):
        valid_datetime = datetime.strptime(request.POST['date_realisation'], '%d/%m/%Y')
        frais.date_realisation = valid_datetime
    else:
        frais.date_realisation = None
    form = FraisMaintenanceForm(data=request.POST)
    previous = request.POST.get('previous', None)
    if form.is_valid():

        frais.save()

        if previous == 'batiment':
            return HttpResponseRedirect(reverse('batiment', args=(batiment_id, )))
        if previous == 'location':
            return HttpResponseRedirect(reverse('location-prepare-update-all', args=(frais.contrat_location.id, )))
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
            fonction = mdl.fonction.Fonction(nom_fonction=new_value)
            fonction.save()
            return fonction
    else:
        fonction_id = get_key(request.POST.get('new_fonction', None))
        return get_object_or_404(mdl.fonction.Fonction, pk=fonction_id)
    return None


def get_societe(request):
    if is_new_value(request.POST.get('new_societe', None)):
        new_value = request.POST.get('new_societe', None)
        if new_value:
            societe = mdl.societe.Societe(nom=new_value)
            societe.save()
            return societe
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
    return render(request, "fraismaintenance_list.html",
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
    return prepare_update(request, id, BATIMENT)


def prepare_update_from_location(request, id):
    return prepare_update(request, id, LOCATION)


def prepare_update_from_dashboard(request, id):
    return prepare_update(request, id, DASHBOARD)


def prepare_update_from_list(request, id):
    return prepare_update(request, id, LISTE)


def delete_frais_from_batiment(request, id):
    return delete_frais(request, id, BATIMENT)


def delete_frais_from_location(request, id):
    return delete_frais(request, id, LOCATION)


def delete_frais_from_list(request, id):
    return delete_frais(request, id, LISTE)
