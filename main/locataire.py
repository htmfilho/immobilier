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
from django.shortcuts import render, get_object_or_404
from main.views_utils import get_key
from main import models as mdl
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from main.pages_utils import NEW, UPDATE, LOCATAIRE_FORM_HTML


@login_required
def locataire_form(request, id):
    locataire = get_object_or_404(mdl.locataire.Locataire, pk=id)
    next = request.META.get('HTTP_REFERER', '/')
    return render(request, LOCATAIRE_FORM_HTML,
                  {'locataire': locataire,
                   'personne':  locataire.personne,
                   'action':    UPDATE,
                   'personnes': mdl.personne.find_all(),
                   'societes':  mdl.societe.find_all(),
                   'fonctions': mdl.fonction.find_all(),
                   'next': next,
                   'localites': mdl.localite.find_all()})


@login_required
def update(request, id):
    locataire = get_object_or_404(mdl.locataire.Locataire, pk=id)
    return render(request, LOCATAIRE_FORM_HTML,
                  {'action':    UPDATE,
                   'locataire': locataire,
                   'personnes': mdl.personne.find_all(),
                   'personne':  locataire.personne,
                   'localites': mdl.localite.find_all()})


@login_required
def new(request, location_id):
    location = get_object_or_404(mdl.contrat_location.ContratLocation, pk=location_id)
    locataire = mdl.locataire.Locataire()
    locataire.contrat_location = location

    return render(request, LOCATAIRE_FORM_HTML,
                  {'locataire': locataire,
                   'location':  location,
                   'personnes': get_personnes_non_locataires(location),
                   'societes':  mdl.societe.find_all(),
                   'action':    UPDATE,
                   'fonctions': mdl.fonction.find_all(),
                   'localites': mdl.localite.find_all()})


def get_personnes_non_locataires(location):
    personnes = mdl.personne.find_all()
    l = []
    if personnes:
        for p in personnes:
            l.append(p)

        for loca in location.locataires:
            l.remove(loca.personne)
    return l


@login_required
def new_without_known_location(request):
    return render(request, LOCATAIRE_FORM_HTML,
                  {'locataire': mdl.locataire.Locataire(),
                   'locations': mdl.contrat_location.find_all(),
                   'personnes': mdl.personne.find_all(),
                   'societes':  mdl.societe.find_all(),
                   'fonctions': mdl.fonction.find_all(),
                   'localites': mdl.localite.find_all(),
                   'action':    NEW})


@login_required
def add(request):
    print('add locataire')
    locataire_id = get_key(request.POST.get('locataire_id', None))
    location_id = request.POST.get('location_id', None)
    personne_id = get_key(request.POST.get('personne_id', None))

    locataire = populate_locataire(locataire_id, location_id, personne_id, request)
    locataire.save()

    action = request.POST.get('action', None)
    if action == UPDATE:
        return render(request, "contratlocation_update.html", {'location': locataire.contrat_location})
    else:
        return HttpResponseRedirect(reverse('home'))


def populate_locataire(locataire_id, location_id, personne_id, request):
    locataire = _get_locataire(locataire_id)
    location = _get_location(location_id)
    locataire.contrat_location = location
    locataire.personne = set_personne(personne_id)
    locataire.principal = False
    if request.POST.get('principal', None) and request.POST['principal'] == 'on':
        locataire.principal = True
    locataire.actif = False
    if request.POST.get('actif', None) and request.POST['actif'] == 'on':
        locataire.actif = True
    locataire.civilite = request.POST['civilite']
    locataire.infos_complement = request.POST['infos_complement']
    locataire.societe = get_societe(request)
    locataire.tva = request.POST['tva']
    fonction_locataire = None
    if request.POST['profession']:
        try:
            id_fonction = int(request.POST['profession'])
            fonction_locataire = mdl.fonction.find_by_id(id_fonction)
        except:
            pass

    locataire.profession = fonction_locataire
    locataire.contrat_location = location
    return locataire


def get_societe(request):
    if request.POST['societe']:
        return get_object_or_404(mdl.societe.Societe, pk=request.POST['societe'])
    return None


def set_personne(personne_id):
    if personne_id:
        return get_object_or_404(mdl.personne.Personne, pk=personne_id)
    return None


@login_required
def delete(request, locataire_id):
    locataire = get_object_or_404(mdl.locataire.Locataire, pk=locataire_id)
    location = locataire.contrat_location
    locataire.delete()
    return render(request, "contratlocation_update.html",
                  {'location': location})


def personne_create(request):
    location_id = request.POST.get('location_id_pers', None)
    action = request.POST.get('action_current', None)
    locataire = mdl.locataire.Locataire()
    location = None
    if location_id:
        location = get_object_or_404(mdl.contrat_location.ContratLocation, pk=location_id)
        locataire.contrat_location = location

    locataire.personne = _save_personne(request)
    personnes = mdl.personne.find_all()

    return render(request, LOCATAIRE_FORM_HTML,
                  {'locataire': locataire,
                   'location': location,
                   'personnes': personnes,
                   'societes': mdl.societe.find_all(),
                   'locations': mdl.contrat_location.find_all(),
                   'fonctions': mdl.fonction.find_all(),
                   'action': action})


def _save_personne(request):
    personne = mdl.personne.Personne(nom=request.POST.get('nom', None),
                                     prenom=request.POST.get('prenom', None),
                                     prenom2=request.POST.get('prenom2', None))
    personne.save()
    return personne


@login_required
def list(request):
    return render(request, "locataire_list.html",
                  {'locataires': mdl.locataire.find_all(),
                   'personnes': mdl.personne.find_all()})


def _get_locataire(locataire_id):
    if locataire_id:
        return get_object_or_404(mdl.locataire.Locataire, pk=locataire_id)
    return mdl.locataire.Locataire()


def _get_location(location_id):
    if location_id:
        return get_object_or_404(mdl.contrat_location.ContratLocation, pk=location_id)
    return None
