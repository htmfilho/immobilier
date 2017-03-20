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
from django.shortcuts import redirect
from main import models as mdl


def liste_proprietaires(request):
    proprietaires = mdl.proprietaire.find_all()
    return render(request, 'listeProprietaires.html', {'proprietaires': proprietaires})


def proprietaire(request, proprietaire_id):
    a_proprietaire = mdl.proprietaire.find_proprietaire(proprietaire_id)
    return render(request, "proprietaire_form.html",
                  {'proprietaire': a_proprietaire,
                   'action': 'update',
                   'personnes': mdl.personne.find_all(),
                   'prev': request.GET.get('prev'),
                   'personne': a_proprietaire.proprietaire})


def add_proprietaire(request, batiment_id):
    """
    Ajoute un propriétaire à un batiment existantes
    ok - 1
    """
    prev = None
    if batiment_id:
        prev = "fb"

    batiment = get_object_or_404(mdl.batiment.Batiment, pk=batiment_id)
    proprietaire = mdl.proprietaire.Proprietaire()
    proprietaire.batiment = batiment
    return render(request, "proprietaire_form.html",
                  {'proprietaire': proprietaire,
                   'action':       'add',
                   'personnes':    mdl.personne.find_all(),
                   "prev": prev})


def update_proprietaire(request, proprietaire_id):
    proprietaire = mdl.proprietaire.find_proprietaire(proprietaire_id)
    return render(request, "proprietaire_form.html",
                  {'proprietaire':         proprietaire,
                   'action':               'update'})


def delete_proprietaire_batiment(request, proprietaire_id):
    print('delete_proprietaire_batiment')
    proprietaire = mdl.proprietaire.find_proprietaire(proprietaire_id)
    batiment = proprietaire.batiment
    proprietaire.delete()

    return render(request, "batiment_form.html", {'batiment': batiment})


def delete_proprietaire(request, proprietaire_id):
    proprietaire = mdl.proprietaire.find_proprietaire(proprietaire_id)
    batiment = proprietaire.batiment
    proprietaire.delete()
    print(request)
    # if '/p/' in request.get_full_path():
    #     print('if')
    #     return render(request, "proprietaire_form.html",
    #                   {'proprietaire':         proprietaire})
    # if '/pl/' in request.get_full_path():
    #     return  listeProprietaires

    if not request.POST.get('prev', None) is None:
        return redirections(request, batiment)

    return render(request, "proprietaire_form.html",
                  {'proprietaire':         proprietaire})


def proprietaire_update_save(request):
    previous = request.POST['previous']
    print('previous:', previous)
    proprietaire = None
    if 'update' == request.POST.get('action', None):
        proprietaire = get_object_or_404(mdl.proprietaire.Proprietaire, pk=request.POST['id'])
    if 'add' == request.POST.get('action', None):
        proprietaire = mdl.proprietaire.Proprietaire()

    if request.POST['date_debut']:
        proprietaire.date_debut = datetime.strptime(request.POST['date_debut'], '%d/%m/%Y')
    if request.POST['date_fin']:
        proprietaire.date_fin = datetime.strptime(request.POST['date_fin'], '%d/%m/%Y')

    personne = get_object_or_404(mdl.personne.Personne, pk=request.POST['proprietaire'])
    proprietaire.proprietaire = personne
    if 'add' == request.POST.get('action', None):
        batiment = get_object_or_404(mdl.batiment.Batiment, pk=request.POST['batiment_id'])
        proprietaire.batiment = batiment
    if not proprietaire.date_debut is None and not proprietaire.date_fin is None:
        if proprietaire.date_debut > proprietaire.date_fin:
            return render(request, "proprietaire_form.html",
                          {'proprietaire': proprietaire,
                           'message': 'La date de début doit être < à la date de fin'})
    proprietaire.save()
    # if 'add' == request.POST.get('action', None):
    #     batiments = Batiment.objects.all()
    #     return render(request, 'listeBatiments.html', {'batiments': batiments})
    if previous:
        # return HttpResponseRedirect(previous)
        print('ici', previous)

        return redirect(previous)
    if not request.POST['prev'] is None:
        return redirections(request, proprietaire.batiment)


def redirections(request, batiment):
    print('redirection', request.POST.get('prev', None))
    if request.POST.get('prev', None) == 'lp':
        return liste_proprietaires(request)
    if request.POST.get('prev', None) == 'fb':
        return render(request, "batiment_form.html",
                      {'batiment': batiment})


def proprietaire_create_for_batiment(request, batiment_id):
    batiment = get_object_or_404(mdl.batiment.Batiment, pk=batiment_id)
    proprietaire = mdl.proprietaire.Proprietaire()
    if batiment:
        proprietaire.batiment = batiment
    personnes = mdl.personne.find_all()

    return render(request, "proprietaire_form.html",
                  {'proprietaire':         proprietaire,
                   'personnes':            personnes,
                   'action':               'add'})


def personne_create(request):
    print('personne_create')
    proprietaire = get_object_or_404(mdl.proprietaire.Proprietaire, pk=request.POST['proprietaire_id_pers'])
    personne = mdl.personne.Personne()
    personne.nom = request.POST['nom']
    personne.prenom = request.POST['prenom']
    personne.save()
    print(personne)
    proprietaire.personne = personne
    personnes = mdl.personne.find_all()

    return render(request, "proprietaire_form.html",
                  {'proprietaire': proprietaire,
                   'personnes': personnes})
