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
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from main.forms import PersonneForm
from main import models as mdl


def edit(request, personne_id):
    if personne_id:
        personne = mdl.personne.find_personne(personne_id)
    else:
        personne = mdl.personne.Personne()
    return render(request, "personne_form.html",
                  {'personne': personne,
                   'societes': mdl.societe.find_all()})


def create(request):
    return render(request, "personne_form.html",
                  {'personne': mdl.personne.Personne(),
                   'societes': mdl.societe.find_all()})


def list(request):
    return render(request, "personne_list.html",
                  {'personnes': mdl.personne.find_all()})


def search(request):
    nom = request.GET.get('nom')
    prenom = request.GET.get('prenom')

    query = mdl.personne.find_all()

    if nom:
        query = query.filter(nom__icontains=nom)
    if prenom:
        query = query.filter(prenom__icontains=prenom)

    return render(request, "personne_list.html",
                  {'nom': nom,
                   'prenom': prenom,
                   'personnes': query})


def update(request):
    form = PersonneForm(data=request.POST)
    if request.POST['personne_id'] and not request.POST['personne_id'] == 'None':
        personne = get_object_or_404(mdl.personne.Personne, pk=request.POST['personne_id'])
    else:
        personne = mdl.personne.Personne()

    personne.nom = request.POST['nom']
    personne.prenom = request.POST['prenom']
    personne.email = request.POST['email']
    personne.personne_type = 'NON_PRECISE'
    if request.POST['type_personne']:
        personne.personne_type = request.POST['type_personne']

    personne.profession = request.POST['profession']
    personne.societe = None
    if request.POST.get('societe', None):
        if request.POST['societe'] != '':
            societe = mdl.societe.find_by_id(int(request.POST['societe']))
            personne.societe = societe

    personne.lieu_naissance = request.POST['lieu_naissance']
    personne.pays_naissance = request.POST['pays_naissance']
    personne.num_identite = request.POST['num_identite']
    personne.num_compte_banque = request.POST['num_compte_banque']

    personne.telephone = request.POST['telephone']
    personne.gsm = request.POST['gsm']
    if request.POST['date_naissance']:
        try:
            personne.date_naissance = datetime.strptime(request.POST['date_naissance'], '%d/%m/%Y')
        except ValueError:
            personne.date_naissance = request.POST['date_naissance']
    else:
        personne.date_naissance = None
    if form.is_valid():
        personne.save()
        return render(request, "personne_list.html",
                      {'personnes': mdl.personne.find_all()})
    else:
        return render(request, "personne_form.html",
                      {'personne': personne,
                       'form': form,
                       'societes': mdl.societe.find_all()})
