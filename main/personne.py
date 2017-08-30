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
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
import json


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
    previous = request.POST.get('previous', None)

    if form.is_valid():
        personne.save()
        batiment_id = get_batiment_id(previous)
        if batiment_id:
            return HttpResponseRedirect(reverse('batiment', args=(batiment_id, )))
        else:
            return render(request, "personne/personne_list.html",
                          {'personnes': mdl.personne.find_all()})
    else:
        return render(request, "personne/personne_form.html",
                      {'personne': personne,
                       'form': form,
                       'pays': mdl.pays.find_all(),
                       'societes': mdl.societe.find_all()})


def get_batiment_id(previous):
    if previous:
        try:
            pos1 = previous.index('/batiment/')
            if pos1 != -1:
                pos1 = pos1 + len('/batiment/')
                pos2 = previous.index('/', pos1)
                if pos2 != -1:
                    return previous[pos1:pos2]
        except:
            return None
    return None


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
    personne.titre = request.POST['titre']
    return personne


def populate_profession(fonction):
    if fonction:
        return fonction.nom_fonction
    return None


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
        return mdl.pays.find_by_id(int(pays_naissance_id))
    return None


def get_societe(request):
    if request.POST['societe'] == '-':
        societe = mdl.societe.Societe(nom=request.POST.get('nom_nouvelle_societe', None),
                                      description=request.POST.get('description_nouvelle_societe', None))
        societe.save()
        return societe
    else:
        return mdl.societe.find_by_id(int(request.POST['societe']))


def get_fonction(request):
    fonction_id = get_key(request.POST['profession'])

    if fonction_id:
        return mdl.fonction.find_by_id(fonction_id)
    else:
        nouvelle_fonction = request.POST.get('profession', None)
        if nouvelle_fonction and len(nouvelle_fonction) > 2:
            fonction_existante = mdl.fonction.find_by_nom(nouvelle_fonction)
            if fonction_existante is None:
                fonction = mdl.fonction.Fonction(nom_fonction=nouvelle_fonction)
                return fonction.save()
    return None


def validate_personne(request):
    nom = request.POST.get('nom', None)
    prenom = request.POST.get('prenom', None)
    prenom2 = request.POST.get('prenom2', None)
    personnes = mdl.personne.find_personne_by_nom_prenom(nom, prenom, prenom2)
    print('validate_personne {} {} {}'.format(nom, prenom, prenom2))
    nom = request.GET.get('nom', None)
    prenom = request.GET.get('prenom', None)
    prenom2 = request.GET.get('prenom2', None)
    print('validate_personne {} {} {}'.format(nom, prenom, prenom2))
    personnes = mdl.personne.find_personne_by_nom_prenom(nom, prenom, prenom2)
    print(personnes)
    if personnes:
        print('validate_personne False')
        return HttpResponse(json.dumps({'valide': False}), content_type='application/json')
        # return False
    print('validate_personne True')
    return HttpResponse(json.dumps({'valide': True}), content_type='application/json')

