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
from main import pages_utils
from main.pages_utils import NEW, UPDATE


def liste_proprietaires(request):
    proprietaires = mdl.proprietaire.find_all()
    return render(request, 'listeProprietaires.html', {'proprietaires': proprietaires})


def proprietaire(request, proprietaire_id):
    a_proprietaire = mdl.proprietaire.find_proprietaire(proprietaire_id)
    return render(request, "proprietaire_form.html",
                  {'proprietaire': a_proprietaire,
                   'action': UPDATE,
                   'personnes': get_personnes_possible(a_proprietaire.batiment),
                   'prev': request.GET.get('prev'),
                   'societes': mdl.societe.find_all_with_name(),
                   'fonctions': mdl.fonction.find_all(),
                   'personne': a_proprietaire.proprietaire,
                   'pays': mdl.pays.find_all()})


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
                   'personnes':    get_personnes_possible(batiment),
                   "prev": prev})


def update_proprietaire(request, proprietaire_id):
    proprietaire = mdl.proprietaire.find_proprietaire(proprietaire_id)
    return render(request, "proprietaire_form.html",
                  {'proprietaire': proprietaire,
                   'action':       UPDATE})


def delete_proprietaire_batiment(request, proprietaire_id):
    print('delete_proprietaire_batiment')
    proprietaire = mdl.proprietaire.find_proprietaire(proprietaire_id)
    batiment = proprietaire.batiment
    proprietaire.delete()

    return render(request, pages_utils.PAGE_BATIMENT_FORM, {'batiment': batiment})


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
                  {'proprietaire': proprietaire,
                   'pays': mdl.pays.find_all()})


def proprietaire_update_save(request):
    previous = request.POST['previous']
    print('previous:', previous)
    proprietaire = None
    action = request.POST.get('action', None)
    if 'update' == action:
        proprietaire = get_object_or_404(mdl.proprietaire.Proprietaire, pk=request.POST['id'])
    if 'add' == action:
        proprietaire = mdl.proprietaire.Proprietaire()
        batiment = get_object_or_404(mdl.batiment.Batiment, pk=request.POST['batiment_id'])
        proprietaire.batiment = batiment

    if request.POST['date_debut']:
        proprietaire.date_debut = datetime.strptime(request.POST['date_debut'], '%d/%m/%Y')
    if request.POST['date_fin']:
        proprietaire.date_fin = datetime.strptime(request.POST['date_fin'], '%d/%m/%Y')

    if request.POST.get('proprietaire') is None or request.POST.get('proprietaire') == '-':
        valide = True
        if request.POST['nouveau_nom'] and request.POST['nouveau_prenom']:
            personne_deja_existante = mdl.personne.find_personne_by_nom_prenom(request.POST['nouveau_nom'],
                                                                               request.POST['nouveau_prenom'],
                                                                               request.POST['nouveau_prenom2'])
            if personne_deja_existante:
                valide = False
                message = 'Une personne existe déjà avec ces noms/prénoms : {} {}'.format(request.POST['nouveau_nom'],
                                                                                          request.POST['nouveau_prenom'])
            else:
                personne = mdl.personne.Personne(nom=request.POST['nouveau_nom'],
                                                 prenom=request.POST['nouveau_prenom'])
                personne.save()
        else:
            message = 'Il faut sélectionner un propriétaire ou créer une nouvelle personne'
            valide = False

        if not valide:
            return render(request, "proprietaire_form.html",
                          {'proprietaire': proprietaire,
                           'action': action,
                           'personnes': get_personnes_possible(proprietaire.batiment),
                           'previous': previous,
                           'message': message,
                           'pays': mdl.pays.find_all()})
    else:
        personne = get_object_or_404(mdl.personne.Personne, pk=request.POST.get('proprietaire', None))

    proprietaire.proprietaire = personne

    if proprietaire.date_debut and proprietaire.date_fin:
        if proprietaire.date_debut > proprietaire.date_fin:
            return render(request, "proprietaire_form.html",
                          {'proprietaire': proprietaire,
                           'action': action,
                           'personnes': get_personnes_possible(proprietaire.batiment),
                           'previous': previous,
                           'message': 'La date de début doit être < à la date de fin',
                           'pays': mdl.pays.find_all()})
    proprietaire.save()
    print(previous)
    if previous:
        return redirect(previous)
    if not request.POST['prev'] is None:
        return redirections(request, proprietaire.batiment)


def redirections(request, batiment):
    print('redirection', request.POST.get('prev', None))
    if request.POST.get('prev', None) == 'lp':
        return liste_proprietaires(request)
    if request.POST.get('prev', None) == 'fb':
        return render(request, pages_utils.PAGE_BATIMENT_FORM,
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
                   'action':               'add',
                   'pays': mdl.pays.find_all()})


def personne_create(request):
    proprietaire = get_object_or_404(mdl.proprietaire.Proprietaire, pk=request.POST['proprietaire_id_pers'])
    personne = mdl.personne.Personne()
    personne.nom = request.POST['nom']
    personne.prenom = request.POST['prenom']
    personne.save()
    proprietaire.personne = personne
    personnes = mdl.personne.find_all()

    return render(request, "proprietaire_form.html",
                  {'proprietaire': proprietaire,
                   'personnes': personnes,
                   'pays': mdl.pays.find_all()})


def get_personnes_possible(batiment):
    personnes_non_encore_proprietaire = []
    personnes = mdl.personne.find_all()
    for p in personnes:
        proprietaires = mdl.proprietaire.search(p, batiment)
        if not proprietaires.exists():
            personnes_non_encore_proprietaire.append(p)
    return personnes_non_encore_proprietaire
