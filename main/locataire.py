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
from main import models as mdl
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from main.pages_utils import NEW, UPDATE, LOCATAIRE_FORM_HTML
from main.forms.locataire import LocataireForm
from main.forms.personne_form import PersonneSimplifieForm
from django.http import HttpResponseRedirect


def get_common_data():
    return {
        'type_societes': mdl.type_societe.find_all(),
        'localites': mdl.localite.find_all(),
        'fonctions': mdl.fonction.find_all(),
        'personnes': mdl.personne.find_all(),
        'societes': mdl.societe.find_all(),
    }


@login_required
def locataire_form(request, id):

    locataire = get_object_or_404(mdl.locataire.Locataire, pk=id)
    form = LocataireForm(instance=locataire)

    next = request.META.get('HTTP_REFERER', '/')

    data = {
        'locataire': locataire,
        'personne': locataire.personne,
        'action': UPDATE,
        'next': next,
        'form': form,
        'form_personne_simplifiee': PersonneSimplifieForm(request.POST or None)
    }
    data.update(get_common_data())
    return render(request,
                  LOCATAIRE_FORM_HTML,
                  data
                  )


@login_required
def update(request, id):
    locataire = get_object_or_404(mdl.locataire.Locataire, pk=id)
    form = LocataireForm(data=request.POST, instance=locataire)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('location-prepare-update-all', args=(locataire.contrat_location.id,)))
    else:
        data = {
            'action': UPDATE,
            'locataire': locataire,
            'personne': locataire.personne,
            'form': form
        }
        data.update(get_common_data())
        return render(request, LOCATAIRE_FORM_HTML,
                      data)


@login_required
def new(request, location_id):
    location = get_object_or_404(mdl.contrat_location.ContratLocation, pk=location_id)
    locataire = mdl.locataire.Locataire()
    locataire.contrat_location = location
    form = LocataireForm(initial={'contrat_location': location})

    data = {'locataire': locataire,
            'location': location,
            'action': UPDATE,
            'form': form,
            'form_personne_simplifiee': PersonneSimplifieForm(request.POST or None)}
    data.update(get_common_data())

    return render(request, LOCATAIRE_FORM_HTML,
                  data)


@login_required
def new_without_known_location(request):
    data = {
        'locataire': mdl.locataire.Locataire(),
        'locations': mdl.contrat_location.find_all(),
        'action': NEW,
        'form': LocataireForm()
    }
    data.update(get_common_data())
    return render(request, LOCATAIRE_FORM_HTML,
                  data)


@login_required
def add(request):
    form_locataire = LocataireForm(data=request.POST)
    personne_form = PersonneSimplifieForm(request.POST or None)

    if form_locataire.is_valid() and personne_form.is_valid():
        personne = request.POST.get('personne')
        if personne:
            locataire = form_locataire.save()
        else:
            personne = personne_form.save()
            locataire = form_locataire.save(commit=False)
            locataire.personne = personne
            locataire.save()

        action = request.POST.get('action', None)
        if action == UPDATE:
            return render(request, "contratlocation_update.html", {'location': locataire.contrat_location})

        else:
            return HttpResponseRedirect(reverse('home'))
    else:
        location_id = request.POST.get('location_id', None)
        location = get_object_or_404(mdl.contrat_location.ContratLocation, pk=location_id)
        locataire = mdl.locataire.Locataire()
        locataire.contrat_location = location
        data = {'locataire': locataire,
                'location': location,
                'action': UPDATE,
                'form': form_locataire,
                'form_personne_simplifiee': personne_form}
        data.update(get_common_data())

        return render(request, LOCATAIRE_FORM_HTML,
                      data)


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
    form = LocataireForm(data=request.POST,
                         initial={'contrat_location': location})
    if location_id:
        location = get_object_or_404(mdl.contrat_location.ContratLocation, pk=location_id)
        locataire.contrat_location = location

    locataire.personne = _save_personne(request)

    data = {
        'locataire': locataire,
        'location': location,
        'locations': mdl.contrat_location.find_all(),
        'action': action,
        'form': form
    }
    data.update(get_common_data())
    return render(request, LOCATAIRE_FORM_HTML,
                  data)


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
