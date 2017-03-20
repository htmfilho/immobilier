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
    frais = mdl.frais_maintenance.FraisMaintenance()
    previous = request.POST.get('previous', None)

    return render(request, "fraismaintenance_form.html",
                  {'frais':     frais,
                   'personnes': mdl.personne.find_all(),
                   'action':   'new',
                   'batiments': mdl.batiment.find_all(),
                   'contrats_location': mdl.contrat_location.find_all(),
                   'entrepreneurs': mdl.professionnel.find_all(),
                   'previous':  previous})


def create(request, batiment_id):
    batiment = get_object_or_404(mdl.batiment.Batiment, pk=batiment_id)
    frais = mdl.frais_maintenance.FraisMaintenance()
    frais.batiment = batiment

    return render(request, "fraismaintenance_form.html",
                  {'frais':     frais,
                   'personnes': mdl.personne.find_all(),
                   'action':   'new',
                   'entrepreneurs': mdl.professionnel.find_all()})


def prepare_update(request, id):
    frais = mdl.frais_maintenance.find_by_id(id)
    return render(request, "fraismaintenance_form.html",
                  {'frais':  frais,
                   'action': 'update',
                   'entrepreneurs': mdl.professionnel.find_all()})


def update(request):
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
    entrepreneur = get_key(request.POST.get('entrepreneur', None))
    if entrepreneur:
        professionnel = get_object_or_404(mdl.professionnel.Professionnel, pk=entrepreneur)

    frais.entrepreneur = professionnel
    if request.POST.get('societe', None):
        frais.societe = request.POST['societe']
    else:
        frais.societe = None
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
        frais.save()
        previous = request.POST.get('previous', None)
        return redirect(previous)
    else:
        return render(request, "fraismaintenance_form.html", {
            'frais': frais,
            'form': form,
            'action': 'update',
            'entrepreneurs': mdl.professionnel.find_all()})


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
    frais = mdl.frais_maintenance.FraisMaintenance()
    previous = request.POST.get('previous', None)
    location = get_object_or_404(mdl.contrat_location.ContratLocation, pk=contrat_location_id)
    if location:
        frais.contrat_location = location
        frais.batiment = location.batiment
    return render(request, "fraismaintenance_form.html",
                  {'frais':             frais,
                   'personnes':         mdl.personne.find_all(),
                   'action':            'new',
                   'batiments':         mdl.batiment.find_all(),
                   'contrats_location': mdl.contrat_location.find_all(),
                   'entrepreneurs':     mdl.professionnel.find_all(),
                   'previous':          previous})
