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

MESSAGE_CREE_UNE_NOUVELLE_PERSONNE = 'Il faut sélectionner un propriétaire ou créer une nouvelle personne'


def liste_proprietaires(request):
    proprietaires = mdl.proprietaire.find_all()
    return render(request, 'listeProprietaires.html', {'proprietaires': proprietaires})


def proprietaire(request, proprietaire_id):
    a_proprietaire = mdl.proprietaire.find_proprietaire(proprietaire_id)
    return render(request, "proprietaire_form.html",
                  {'proprietaire': a_proprietaire,
                   'action': UPDATE,
                   'personnes': get_personnes_possibles(a_proprietaire.batiment),
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
                   'personnes':    get_personnes_possibles(batiment),
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

def _get_validation_data(request):
    return {'proprietaire': request.POST.get('proprietaire', None),
            'nouveau_nom': request.POST.get('nouveau_nom', None),
            'nouveau_prenom': request.POST.get('nouveau_prenom', None),
            'nouveau_prenom2': request.POST.get('nouveau_prenom2', None),
            }

def _validation(data_to_validated, proprietaire):
    if _no_existing_prorietaire_selected(data_to_validated['proprietaire']):
        nouveau_nom = data_to_validated['nouveau_nom']
        nouveau_prenom = data_to_validated['nouveau_prenom']
        if _new_parameters_ok(nouveau_nom, nouveau_prenom):
            personne_deja_existante = mdl.personne \
                .find_personne_by_nom_prenom(nouveau_nom,
                                             nouveau_prenom,
                                             data_to_validated['nouveau_prenom2'])
            if personne_deja_existante:
                return 'Une personne existe déjà avec ces noms/prénoms : {} {}' \
                    .format(nouveau_nom, nouveau_prenom)
        else:
            return MESSAGE_CREE_UNE_NOUVELLE_PERSONNE

    if not _date_is_valide(proprietaire):
        return 'La date de début doit être < à la date de fin.  Merci de corriger avant de sauvegarder.'

    return None


def _new_parameters_ok(nouveau_nom, nouveau_prenom):
    if nouveau_nom and nouveau_prenom:
        if len(nouveau_nom.lstrip()) > 0 and len(nouveau_prenom.lstrip()) > 0:
            return True
    return False


def _no_existing_prorietaire_selected(proprietaire_field):
    if proprietaire_field is None or proprietaire_field == '-':
        return True
    return False


def _date_is_valide(proprietaire):
    if proprietaire.date_debut and proprietaire.date_fin and proprietaire.date_debut > proprietaire.date_fin:
        return False
    return True


def proprietaire_update_save(request):
    print('proprietaire_update_save')
    previous = request.POST.get('previous', None)
    prev = request.POST.get('prev', None)
    proprietaire = get_proprietaire(request)

    proprietaire.date_debut = get_date(request.POST.get('date_debut', None))
    proprietaire.date_fin = get_date(request.POST.get('date_fin', None))

    valide = True
    message = _validation(_get_validation_data(request), proprietaire)
    if message:
        valide = False
    personne = get_personne_proprietaire(request)
    proprietaire.proprietaire = personne

    if not valide:
        return render(request, "proprietaire_form.html",
                      {'proprietaire': proprietaire,
                       'personnes': get_personnes_possibles(proprietaire.batiment),
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
    proprietaire.personne = mdl.personne.creation_nouvelle_personne(request.POST['nom'], request.POST['prenom'])
    personnes = mdl.personne.find_all()

    return render(request, "proprietaire_form.html",
                  {'proprietaire': proprietaire,
                   'personnes': personnes,
                   'pays': mdl.pays.find_all()})


def get_personnes_possibles(batiment):
    personnes_non_encore_proprietaire = []
    for p in mdl.personne.find_all():
        proprietaires = mdl.proprietaire.search(p, batiment)
        if not proprietaires.exists():
            personnes_non_encore_proprietaire.append(p)
    return personnes_non_encore_proprietaire
