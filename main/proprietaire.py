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
from django.shortcuts import redirect
from main import models as mdl
from main import pages_utils
from main.pages_utils import UPDATE
from main.views_utils import get_date, get_key


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
    proprietaire = mdl.proprietaire.find_proprietaire(proprietaire_id)
    batiment = proprietaire.batiment
    proprietaire.delete()

    return render(request, pages_utils.PAGE_BATIMENT_FORM, {'batiment': batiment})


def delete_proprietaire(request, proprietaire_id):
    proprietaire = mdl.proprietaire.find_proprietaire(proprietaire_id)
    batiment = proprietaire.batiment
    proprietaire.delete()
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


def validation(request, proprietaire):
    if request.POST.get('proprietaire', None) is None or request.POST.get('proprietaire', None) == '-':
        if request.POST.get('nouveau_nom', None) and request.POST.get('nouveau_prenom', None):
            personne_deja_existante = mdl.personne \
                .find_personne_by_nom_prenom(request.POST.get('nouveau_nom', None),
                                             request.POST.get('nouveau_prenom', None),
                                             request.POST.get('nouveau_prenom2', None))
            if personne_deja_existante:
                return 'Une personne existe déjà avec ces noms/prénoms : {} {}' \
                    .format(request.POST['nouveau_nom'], request.POST['nouveau_prenom'])

        else:
            return 'Il faut sélectionner un propriétaire ou créer une nouvelle personne'

    if proprietaire.date_debut and proprietaire.date_fin and proprietaire.date_debut > proprietaire.date_fin:
        return 'La date de début doit être < à la date de fin.  Merci de corriger avant de sauvegarder.'

    return None


def proprietaire_update_save(request):
    previous = request.POST.get('previous', None)
    prev = request.POST.get('prev', None)
    proprietaire = get_proprietaire(request)

    proprietaire.date_debut = get_date(request.POST.get('date_debut', None))
    proprietaire.date_fin = get_date(request.POST.get('date_fin', None))

    valide = True
    message = validation(request, proprietaire)
    if message:
        valide = False
    personne = get_personne_proprietaire(request)
    proprietaire.proprietaire = personne

    if not valide:
        return render(request, "proprietaire_form.html",
                      {'proprietaire': proprietaire,
                       'personnes': get_personnes_possible(proprietaire.batiment),
                       'previous': previous,
                       'prev': prev,
                       'message': message,
                       'pays': mdl.pays.find_all(),
                       'personne': personne})

    proprietaire.save()
    return redirection_apres_update(request, previous, proprietaire)


def get_proprietaire(request):
    an_id = get_key(request.POST.get('id', None))
    if an_id:
        proprietaire = get_object_or_404(mdl.proprietaire.Proprietaire, pk=an_id)
    else:
        proprietaire = initialize_new_proprietaire_with_batiment(request)
    return proprietaire


def get_personne_proprietaire(request):
    if request.POST.get('proprietaire') is None or request.POST.get('proprietaire') == '-':
        if request.POST.get('nouveau_nom', None) and request.POST.get('nouveau_prenom', None):
            personne_deja_existante = mdl.personne.find_personne_by_nom_prenom(request.POST.get('nouveau_nom', None),
                                                                               request.POST.get('nouveau_prenom', None),
                                                                               request.POST.get('nouveau_prenom2',
                                                                                                None))
            if not personne_deja_existante:
                return mdl.personne.creation_nouvelle_personne(request.POST.get('nouveau_nom', None),
                                                               request.POST.get('nouveau_prenom', None))
    else:
        return mdl.personne.find_personne(request.POST.get('proprietaire'))
    return None


def redirection_apres_update(request, previous, proprietaire):
    prev = request.POST.get('prev', None)
    if prev:
        return redirections(request, proprietaire.batiment)
    if previous:
        return redirect(previous)
    return None


def initialize_new_proprietaire_with_batiment(request):
    proprietaire = mdl.proprietaire.Proprietaire()
    batiment = get_object_or_404(mdl.batiment.Batiment, pk=request.POST['batiment_id'])
    proprietaire.batiment = batiment
    return proprietaire


def redirections(request, batiment):
    previous = request.POST.get('prev', None)
    if previous == 'lp':
        return liste_proprietaires(request)
    if previous == 'fb':
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
