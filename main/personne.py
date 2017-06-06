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
from main.views_utils import get_key


def get_personne(personne_id):
    if personne_id and not personne_id == 'None':
        return get_object_or_404(mdl.personne.Personne, pk=personne_id)
    else:
        return mdl.personne.Personne()


def edit(request, personne_id):
    return render(request, "personne_form.html",
                  {'personne': get_personne(personne_id),
                   'fonctions': mdl.fonction.find_all(),
                   'societes': mdl.societe.find_all(),
                   'pays': mdl.pays.find_all()})


def create(request):
    return render(request, "personne_form.html",
                  {'personne': mdl.personne.Personne(),
                   'societes': mdl.societe.find_all(),
                   'pays': mdl.pays.find_all()})


def list(request):
    return render(request, "personne/personne_list.html",
                  {'personnes': mdl.personne.find_all()})


def search(request):
    nom = request.GET.get('nom')
    prenom = request.GET.get('prenom')

    query = mdl.personne.find_all()

    if nom:
        query = query.filter(nom__icontains=nom)
    if prenom:
        query = query.filter(prenom__icontains=prenom)

    return render(request, "personne/personne_list.html",
                  {'nom': nom,
                   'prenom': prenom,
                   'personnes': query})


def update(request):
    form = PersonneForm(data=request.POST)
    personne = get_personne(request.POST.get('personne_id', None))

    personne.nom = request.POST['nom']
    personne.prenom = request.POST['prenom']
    personne.prenom2 = request.POST['prenom2']
    personne.email = request.POST['email']
    personne.personne_type = 'NON_PRECISE'

    fonction = get_fonction(request)
    personne.fonction = fonction
    if fonction:
        personne.profession = fonction.nom_fonction
    else:
        personne.profession = None

    personne.societe = get_societe(request)

    personne.lieu_naissance = request.POST['lieu_naissance']
    pays_naissance_id = request.POST.get('pays_naissance', None)
    print(pays_naissance_id)
    if pays_naissance_id:
        personne.pays_naissance = mdl.pays.find_by_id(pays_naissance_id)
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
        return render(request, "personne/personne_list.html",
                      {'personnes': mdl.personne.find_all()})
    else:
        return render(request, "personne_form.html",
                      {'personne': personne,
                       'form': form,
                       'societes': mdl.societe.find_all()})


def get_societe(request):
    societe = None
    if request.POST['societe'] == '-':
        societe = mdl.societe.Societe(nom=request.POST.get('nom_nouvelle_societe', None),
                                      description=request.POST.get('description_nouvelle_societe', None))
        societe.save()
        return societe
    else:
        return mdl.societe.find_by_id(int(request.POST['societe']))


def get_fonction(request):
    fonction_id = get_key(request.POST['profession'])
    fonction = None
    if fonction_id:
        fonction = mdl.fonction.find_by_id(fonction_id)
    else:
        nouvelle_fonction = request.POST.get('profession', None)
        if nouvelle_fonction and len(nouvelle_fonction) > 0:
            fonction_existante = mdl.fonction.find_by_nom(nouvelle_fonction)
            if fonction_existante is None:
                fonction = mdl.fonction.Fonction(nom_fonction=nouvelle_fonction)
                fonction.save()
    return fonction


