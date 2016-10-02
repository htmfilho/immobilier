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

from django.shortcuts import redirect
from main.models import Personne, ContratLocation, Locataire, Societe, Fonction
from django.shortcuts import render, get_object_or_404


def locataire_form(request, id):
    locataire = get_object_or_404(Locataire, pk=id)
    next = request.META.get('HTTP_REFERER', '/')
    return render(request, "locataire_form.html",
                  {'locataire': locataire,
                   'action':    'update',
                   'personnes': Personne.find_all(),
                   'societes': Societe.find_all(),
                   'fonctions': Fonction.find_all(),
                   'next': next})


def update(request, id):
    locataire = get_object_or_404(Locataire, pk=id)
    return render(request, "locataire_form.html",
                  {'locataire':         locataire,'personne': locataire.personne})


def new(request, location_id):
    print(new)
    print('new locataire', location_id)
    location = get_object_or_404(ContratLocation, pk=location_id)

    locataire = Locataire()
    locataire.contrat_location=location
    personnes = Personne.objects.filter()
    l = []
    if personnes:
        for p in personnes:
            l.append(p)

        for loca in location.locataires:
            l.remove(loca.personne)

    return render(request, "locataire_form.html",
                  {'locataire': locataire,
                   'location' : location,
                   'personnes': l,
                   'societes': Societe.find_all(),
                   'fonctions': Fonction.find_all(),})

def add(request):
    print('add')
    if 'bt_cancel' not in request.POST:
        if request.POST['locataire_id'] and not request.POST['locataire_id']== 'None':
            locataire = get_object_or_404(Locataire, pk=request.POST.get('locataire_id', None))
        else:
            locataire = Locataire()

        location = get_object_or_404(ContratLocation, pk=request.POST.get('location_id', None))
        if request.POST['personne_id']:
            personne = get_object_or_404(Personne, pk=request.POST['personne_id'])
            locataire.personne = personne

        locataire.principal = False
        if request.POST.get('principal',None) and request.POST['principal'] == 'on':
            locataire.principal = True
        locataire.civilite = request.POST['civilite']
        locataire.infos_complement = request.POST['infos_complement']
        societe = None
        if request.POST['societe']:
            societe = get_object_or_404(Societe, pk=request.POST['societe'])
        locataire.societe = societe
        locataire.tva = request.POST['tva']
        fonction = None
        if request.POST['profession']:
            fonction = get_object_or_404(Fonction, pk=request.POST['profession'])
        locataire.profession = fonction

        locataire.contrat_location = location
        locataire.save()
        return render(request, "contratlocation_update.html",
                      {'location': location})
    else:
        return redirect(request.POST.get('next'), None)


def delete(request,locataire_id):
    locataire = get_object_or_404(Locataire, pk=locataire_id)
    location = locataire.contrat_location
    locataire.delete()
    return render(request, "contratlocation_update.html",
                  {'location': location})


def personne_create(request):
    location = get_object_or_404(ContratLocation, pk=request.POST['location_id_pers'])
    locataire = Locataire()
    locataire.contrat_location=location

    personne = Personne()
    personne.nom =request.POST['nom']
    personne.prenom =request.POST['prenom']
    personne.save()
    locataire.personne=personne
    personnes = Personne.objects.filter()

    return render(request, "locataire_form.html",
                  {'locataire': locataire,
                   'location' : location,
                   'personnes': personnes,
                   'societes': Societe.find_all(),
                   'fonctions': Fonction.find_all(),})


def list(request):
    return render(request, "locataire_list.html",
                  {'locataires': Locataire.objects.all(),
                   'personnes': Personne.find_all()})
