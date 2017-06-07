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
    return render(request, "personne/personne_form.html",
                  {'personne': get_personne(personne_id),
                   'fonctions': mdl.fonction.find_all(),
                   'societes': mdl.societe.find_all(),
                   'pays': mdl.pays.find_all()})


def create(request):
    return render(request, "personne/personne_form.html",
                  {'personne': mdl.personne.Personne(),
                   'societes': mdl.societe.find_all(),
                   'pays': mdl.pays.find_all()})


def list(request):
    return render(request, "personne/personne_list.html",
                  {'personnes': mdl.personne.find_all()})


def search(request):
    nom = request.GET.get('nom', None)
    prenom = request.GET.get('prenom', None)
    return render(request, "personne/personne_list.html",
                  {'nom': nom,
                   'prenom': prenom,
                   'personnes':  mdl.personne.search(nom, prenom)})


def update(request):
    form = PersonneForm(data=request.POST)
    personne = populate_personne(request)

    if form.is_valid():
        personne.save()
        return render(request, "personne/personne_list.html",
                      {'personnes': mdl.personne.find_all()})
    else:
        return render(request, "personne/personne_form.html",
                      {'personne': personne,
                       'form': form,
                       'pays': mdl.pays.find_all(),
                       'societes': mdl.societe.find_all()})


def populate_personne(request):
    personne = get_personne(request.POST.get('personne_id', None))
    personne.nom = request.POST['nom']
    personne.prenom = request.POST['prenom']
    personne.prenom2 = request.POST['prenom2']
    personne.email = request.POST['email']
    personne.personne_type = 'NON_PRECISE'
    fonction = get_fonction(request)
    personne.fonction = fonction
    personne.profession = populate_profession(fonction)

    personne.societe = get_societe(request)
    personne.lieu_naissance = request.POST['lieu_naissance']
    personne.pays_naissance = populate_pays_naissance(request)

    personne.num_identite = request.POST['num_identite']
    personne.num_compte_banque = request.POST['num_compte_banque']
    personne.telephone = request.POST['telephone']
    personne.gsm = request.POST['gsm']
    personne.date_naissance = populate_date(request.POST['date_naissance'])
    return personne


def populate_profession(fonction):
    if fonction:
        return fonction.nom_fonction
    return  None


def populate_date(request_value):
    if request_value:
        try:
            return datetime.strptime(request_value, '%d/%m/%Y')
        except ValueError:
            return request_value
    return None


def populate_pays_naissance(request):
    pays_naissance_id = get_key(request.POST.get('pays_naissance', None))
    if pays_naissance_id:
        return  mdl.pays.find_by_id(int(pays_naissance_id))
    return None

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


