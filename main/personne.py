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
from main.forms.forms import PersonneForm
from main import models as mdl
from main.views_utils import get_key
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
import json
from main import societe
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required


PERSONNE_LIST_HTML = "personne/personne_list.html"
PERSONNE_FORM_HTML = "personne/personne_form.html"


def get_personne(personne_id):
    if personne_id and not personne_id == 'None':
        return get_object_or_404(mdl.personne.Personne, pk=personne_id)
    else:
        return mdl.personne.Personne()


def get_common_data(personne_id):
    data = {
        'fonctions': mdl.fonction.find_all(),
        'societes': mdl.societe.find_all(),
        'pays': mdl.pays.find_all(),
        'localites': mdl.localite.find_all(),
        'type_societes': mdl.type_societe.find_all(),
    }
    if personne_id:
        data.update({'personne': get_personne(personne_id)})
    else:
        data.update({'personne': mdl.personne.Personne()})
    return data


@login_required
def edit(request, personne_id):
    return render(request, PERSONNE_FORM_HTML,
                  get_common_data(personne_id))


@login_required
def create(request):
    return render(request, PERSONNE_FORM_HTML,
                  get_common_data(None))


@login_required
def list(request):
    return render(request, PERSONNE_LIST_HTML,
                  {'personnes': mdl.personne.find_all()})


@login_required
@require_http_methods(["GET"])
def search(request):
    nom = request.GET.get('nom', None)
    prenom = request.GET.get('prenom', None)
    return render(request, PERSONNE_LIST_HTML,
                  {'nom': nom,
                   'prenom': prenom,
                   'personnes':  mdl.personne.search(nom, prenom)})


@login_required
@require_http_methods(["POST"])
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
            return render(request, PERSONNE_LIST_HTML,
                          {'personnes': mdl.personne.find_all()})
    else:
        return render(request, PERSONNE_FORM_HTML,
                      {'personne': personne,
                       'form': form,
                       'pays': mdl.pays.find_all(),
                       'societes': mdl.societe.find_all(),
                       'fonctions': mdl.fonction.find_all()})


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


@login_required
@require_http_methods(["POST"])
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

    personne.societe = get_societe(request.POST)
    personne.lieu_naissance = request.POST['lieu_naissance']
    personne.pays_naissance = populate_pays_naissance(request.POST.get('pays_naissance', None))

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


def populate_pays_naissance(pays_naissance_id):
    if pays_naissance_id:
        try:
            return mdl.pays.find_by_id(int(pays_naissance_id))
        except:
            return None
    return None


def get_societe(data):
    if data['societe'] == '-':
        if data.get('nom_nouvelle_societe', None):
            return societe.creation_nouvelle_societe(data.get('nom_nouvelle_societe', None),
                                                     data.get('description_nouvelle_societe', None))
        return None
    else:
        return mdl.societe.find_by_id(int(data['societe']))


@login_required
@require_http_methods(["POST"])
def get_fonction(request):
    fonction_id = get_key(request.POST['profession'])

    if fonction_id:
        return mdl.fonction.find_by_id(fonction_id)
    else:
        nouvelle_fonction = request.POST.get('profession', None)
        if nouvelle_fonction and len(nouvelle_fonction) > 2:
            fonction_existante = mdl.fonction.find_by_nom(nouvelle_fonction)
            if fonction_existante is None:
                return mdl.fonction.create_fonction(nouvelle_fonction)
    return None


@login_required
@require_http_methods(["GET", "POST"])
def validate_personne(request):
    if request.method == 'POST':
        data = request.POST
    else:
        data = request.GET

    nom = data.get('nom', None)
    prenom = data.get('prenom', None)
    prenom2 = data.get('prenom2', None)
    personnes = mdl.personne.find_personne_by_nom_prenom(nom, prenom, prenom2)

    if personnes:
        return HttpResponse(json.dumps({'valide': False}), content_type='application/json')

    return HttpResponse(json.dumps({'valide': True}), content_type='application/json')
