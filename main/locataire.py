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
from main.views_utils import get_key
from main import models as mdl
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


LOCATAIRE_FORM_HTML = "locataire/locataire_form.html"


def locataire_form(request, id):
    locataire = get_object_or_404(mdl.locataire.Locataire, pk=id)
    next = request.META.get('HTTP_REFERER', '/')
    return render(request, LOCATAIRE_FORM_HTML,
                  {'locataire': locataire,
                   'personne': locataire.personne,
                   'action':    'update',
                   'personnes': mdl.personne.find_all(),
                   'societes': mdl.societe.find_all(),
                   'fonctions': mdl.fonction.find_all(),
                   'next': next})


def update(request, id):
    locataire = get_object_or_404(mdl.locataire.Locataire, pk=id)
    return render(request, LOCATAIRE_FORM_HTML,
                  {'action': 'update',
                   'locataire': locataire,
                   'personnes': mdl.personne.find_all(),
                   'personne': locataire.personne})


def new(request, location_id):
    location = get_object_or_404(mdl.contrat_location.ContratLocation, pk=location_id)
    locataire = mdl.locataire.Locataire()
    locataire.contrat_location = location

    return render(request, LOCATAIRE_FORM_HTML,
                  {'locataire': locataire,
                   'location': location,
                   'personnes': get_personnes_non_locataires(location),
                   'societes': mdl.societe.find_all(),
                   'action': 'update',
                   'personnes': mdl.personne.find_all(),
                   'fonctions': mdl.fonction.find_all(), })


def get_personnes_non_locataires(location):
    personnes = mdl.personne.find_all()
    l = []
    if personnes:
        for p in personnes:
            l.append(p)

        for loca in location.locataires:
            l.remove(loca.personne)
    return l


def new_without_known_location(request):
    locataire = mdl.locataire.Locataire()
    return render(request, LOCATAIRE_FORM_HTML,
                  {'locataire': locataire,
                   'locations': mdl.contrat_location.find_all(),
                   'personnes': mdl.personne.find_all(),
                   'societes': mdl.societe.find_all(),
                   'fonctions': mdl.fonction.find_all(), })


def add(request):
    locataire_id = get_key(request.POST.get('locataire_id', None))
    location_id = request.POST.get('location_id', None)
    personne_id = get_key(request.POST.get('personne_id', None))

    locataire = populate_locataire(locataire_id, location_id, personne_id, request)
    locataire.save()

    action = request.POST.get('action', None)
    if action == "update":
        return render(request, "contratlocation_update.html", {'location': locataire.contrat_location})
    else:
        return HttpResponseRedirect(reverse('home'))


def populate_locataire(locataire_id, location_id, personne_id, request):
    locataire = get_locataire(locataire_id)
    location = get_location(location_id)
    locataire.contrat_location = location
    if personne_id:
        personne = get_object_or_404(mdl.personne.Personne, pk=personne_id)
        locataire.personne = personne
    locataire.principal = False
    if request.POST.get('principal', None) and request.POST['principal'] == 'on':
        locataire.principal = True
    locataire.actif = False
    if request.POST.get('actif', None) and request.POST['actif'] == 'on':
        locataire.actif = True
    locataire.civilite = request.POST['civilite']
    locataire.infos_complement = request.POST['infos_complement']
    societe = None
    if request.POST['societe']:
        societe = get_object_or_404(mdl.societe.Societe, pk=request.POST['societe'])
    locataire.societe = societe
    locataire.tva = request.POST['tva']

    if request.POST['profession']:
        try:

            id_fonction = int(request.POST['profession'])
            fonction_locataire = mdl.fonction.find_by_id(id_fonction)
        except:
            fonction_locataire = None

    locataire.profession = fonction_locataire
    locataire.contrat_location = location
    return locataire


def delete(request, locataire_id):
    locataire = get_object_or_404(mdl.locataire.Locataire, pk=locataire_id)
    location = locataire.contrat_location
    locataire.delete()
    return render(request, "contratlocation_update.html",
                  {'location': location})


def personne_create(request):
    location_id = request.POST.get('location_id_pers', None)
    locataire = mdl.locataire.Locataire()
    location = None
    if location_id:
        location = get_object_or_404(mdl.contrat_location.ContratLocation, pk=location_id)
        locataire.contrat_location = location

    personne = mdl.personne.Personne(nom=request.POST.get('nom', None), prenom=request.POST.get('prenom', None))
    personne.save()
    locataire.personne = personne
    personnes = mdl.personne.find_all()

    return render(request, LOCATAIRE_FORM_HTML,
                  {'locataire': locataire,
                   'location': location,
                   'personnes': personnes,
                   'societes': mdl.societe.find_all(),
                   'fonctions': mdl.fonction.find_all(), })


def list(request):
    return render(request, "locataire_list.html",
                  {'locataires': mdl.locataire.find_all(),
                   'personnes': mdl.personne.find_all()})


def get_locataire(locataire_id):
    if locataire_id:
        return get_object_or_404(mdl.locataire.Locataire, pk=locataire_id)
    else:
        return mdl.locataire.Locataire()


def get_location(location_id):
    if location_id:
        return get_object_or_404(mdl.contrat_location.ContratLocation, pk=location_id)

    return None
