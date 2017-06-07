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


def new(request):
    print('new')
    frais = mdl.frais_maintenance.FraisMaintenance()
    previous = request.POST.get('previous', None)

    return render(request, "frais/fraismaintenance_form.html",
                  {'frais':     frais,
                   'personnes': mdl.personne.find_all(),
                   'action':   'new',
                   'batiments': mdl.batiment.find_all(),
                   'contrats_location': mdl.contrat_location.find_all(),
                   'entrepreneurs': mdl.professionnel.find_all(),
                   'societes': mdl.societe.find_all_with_name(),
                   'fonctions': mdl.fonction.find_all(),
                   'previous':  previous})


def create(request, batiment_id):
    print('create')
    batiment = get_object_or_404(mdl.batiment.Batiment, pk=batiment_id)
    frais = mdl.frais_maintenance.FraisMaintenance()
    frais.batiment = batiment

    return render(request, "frais/fraismaintenance_form.html",
                  {'frais':     frais,
                   'personnes': mdl.personne.find_all(),
                   'action':   'new',
                   'entrepreneurs': mdl.professionnel.find_all(),
                   'societes': mdl.societe.find_all_with_name(),
                   'fonctions': mdl.fonction.find_all()
                   })


def prepare_update(request, id):
    print('prepare_update')
    frais = mdl.frais_maintenance.find_by_id(id)
    return render(request, "frais/fraismaintenance_form.html",
                  {'frais':  frais,
                   'action': 'update',
                   'entrepreneurs': mdl.professionnel.find_all()})


def update(request):
    print('frais update')
    batiment_id = get_key(request.POST.get('batiment_id', None))
    if request.POST.get('action', None) == 'new':
        frais = mdl.frais_maintenance.FraisMaintenance()
        if batiment_id:
            batiment = get_object_or_404(mdl.batiment.Batiment, pk=batiment_id)
            frais.batiment = batiment
    else:
        frais = get_object_or_404(mdl.frais_maintenance.FraisMaintenance, pk=request.POST.get('id', None))
        batiment = get_object_or_404(mdl.batiment.Batiment, pk=batiment_id)
        frais.batiment = batiment
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

    print(professionnel)

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
        frais.montant = float(request.POST['montant'].replace(',', '.'))
    else:
        frais.montant = 0
    if request.POST.get('date_realisation', None):
        valid_datetime = datetime.strptime(request.POST['date_realisation'], '%d/%m/%Y')
        frais.date_realisation = valid_datetime
    else:
        frais.date_realisation = None
    form = FraisMaintenanceForm(data=request.POST)

    if form.is_valid():
        print('valid')
        frais.save()
        print(frais.id)
        previous = request.POST.get('previous', None)
        return redirect(previous)
    else:
        print('invalid')
        return render(request, "frais/fraismaintenance_form.html", {
            'frais': frais,
            'form': form,
            'action': 'update',
            'entrepreneurs': mdl.professionnel.find_all()})


def nouveau_professionnel(request):
    # nouvelle entrepreneur

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
        print('personne_ne')
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


def delete(request, id):
    frais = get_object_or_404(mdl.frais_maintenance.FraisMaintenance, pk=id)
    if frais:
        frais.delete()
    return render(request, "fraismaintenance_confirm_delete.html",
                           {'object': frais})


def contrat_new(request, contrat_location_id):
    print('contrat_new')
    frais = mdl.frais_maintenance.FraisMaintenance()
    previous = request.POST.get('previous', None)
    location = get_object_or_404(mdl.contrat_location.ContratLocation, pk=contrat_location_id)
    if location:
        frais.contrat_location = location
        frais.batiment = location.batiment
    return render(request, "frais/fraismaintenance_form.html",
                  {'frais':             frais,
                   'personnes':         mdl.personne.find_all(),
                   'action':            'new',
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

def delete_frais(request, id):
    frais = mdl.frais_maintenance.find_by_id(id)
    batiment = frais.batiment
    if frais:
        frais.delete()

    return render(request, "batiment_form.html", {'batiment': batiment})
