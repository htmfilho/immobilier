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
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from datetime import date
from datetime import datetime
from main.forms import ContratLocationForm
from dateutil.relativedelta import relativedelta
from main import models as mdl
from django.utils import timezone
from main.views_utils import get_key, get_date, UNDEFINED
from django.http import HttpResponseRedirect


CONTRAT_LOCATION_LIST_HTML = "location/contratlocation_list.html"
ONE_YEAR_DURATION = '1'
SEVEN_YEARS_DURATION = '7'


def prepare_update(request, location_id):
    location = mdl.contrat_location.find_by_id(location_id)
    return render(request, "contratlocation_update.html",
                  {'location':    location,
                   'assurances': mdl.assurance.find_all(), })


def update(request):
    previous = request.POST.get('previous', None)
    id = request.POST.get('id', None)
    form = ContratLocationForm(data=request.POST)
    location = get_object_or_404(mdl.contrat_location.ContratLocation, pk=id)
    prolongation_action = prolongation_button_clicked(request)

    location.renonciation = get_date(request.POST.get('renonciation', None))
    location.remarque = request.POST.get('remarque', None)
    location.assurance = get_assurance_location(request.POST['assurance'])

    if form.is_valid():
        data = form.cleaned_data
        if is_prolongation(request.POST.get('type_prolongation', None), prolongation_action):
            # Les financements seront adaptés via le save
            location.save_prolongation(int(request.POST.get('type_prolongation')))
        else:
            date_debut_formulaire = data['date_debut']
            location.save()
        if not prolongation_action:
            return redirect(previous)

    return render(request, "contratlocation_update.html",
                           {'location':    location,
                            'assurances':  mdl.assurance.find_all(),
                            'nav':         'list_batiment',
                            'form':        form,
                            'previous':    previous})


def prolongation_button_clicked(request):
    if 'bt_prolongation' in request.POST:
        return True
    return False


def is_prolongation(type_prolongation, prolongation_action):
    if prolongation_action and (type_prolongation == ONE_YEAR_DURATION or type_prolongation == SEVEN_YEARS_DURATION):
        return True
    return False


def get_assurance_location(assurance_post_value):
    if assurance_post_value and not assurance_post_value == UNDEFINED:
        return mdl.assurance.find_by_id(get_key(assurance_post_value))
    return None


def contrat_location_for_batiment(request, batiment_id):
    batiment = get_object_or_404(mdl.batiment.Batiment, pk=batiment_id)
    if batiment.location_actuelle:
        location = get_object_or_404(mdl.contrat_location.ContratLocation, pk=batiment.location_actuelle.id)
    else:
        location = None
    nouvelle_location = mdl.contrat_location.ContratLocation()
    if batiment:
        nouvelle_location.batiment = batiment
    if location is not None:
        nouvelle_location.date_debut = location.date_fin
        nouvelle_location.date_fin = location.date_fin + relativedelta(years=1)
        nouvelle_location.loyer_base = location.loyer_base
        nouvelle_location.charges_base = location.charges_base
    else:
        auj = date.today()
        nouvelle_location.date_debut = auj.strftime("%d/%m/%Y")

        # le financement sera crée automatiquement
    return render(request, "location/contratlocation_new.html",
                           {'location': nouvelle_location,
                            'assurances': mdl.assurance.find_all(),
                            'nav': 'list_batiment'})


def list(request):
    date_fin = timezone.now().date()
    locations = mdl.contrat_location.search(date_fin)
    return render(request, CONTRAT_LOCATION_LIST_HTML,
                  {'locations': locations,
                   'date_fin_filtre_location': date_fin})


def delete(request, location_id):
    location = get_object_or_404(mdl.contrat_location.ContratLocation, pk=location_id)
    if location:
        location.delete()

    return HttpResponseRedirect(reverse('contratlocation_list'))


def test(request):
    form = ContratLocationForm(data=request.POST)
    batiment = get_batiment(get_key(request.POST.get('batiment_id', None)))

    location = mdl.contrat_location.ContratLocation()
    location.date_debut = None
    location.batiment = batiment
    location.remarque = request.POST.get('remarque', None)
    location.assurance = get_assurance(request)
    location.loyer_base = request.POST['loyer_base']
    location.charges_base = request.POST['charges_base']

    if request.POST['date_debut']:
        location.date_debut = get_date(request.POST.get('date_debut', None))
        locations_en_cours = mdl.contrat_location.find_by_batiment_location(batiment, location.date_debut)
        if locations_en_cours:
            return already_existing_location(form, location, locations_en_cours, request)
        else:
            location.date_fin = location.date_debut + relativedelta(years=1)
            location.renonciation = location.date_debut + relativedelta(days=355)

    if form.is_valid():
        location.save()
        return HttpResponseRedirect(reverse('batiment', args=(location.batiment.id, )))
    else:
        return render(request, "location/contratlocation_form.html",
                               {'location': location,
                                'assurances': mdl.assurance.find_all(),
                                'batiments': mdl.batiment.find_all(),
                                'nav': 'list_batiment',
                                'form': form})


def already_existing_location(form, location, locations_en_cours, request):
    location.date_fin = None
    location.renonciation = None
    location_courante = locations_en_cours.first()
    return render(request, "location/contratlocation_form.html",
                  {'location': location,
                   'assurances': mdl.assurance.find_all(),
                   'nav': 'list_batiment',
                   'batiments': mdl.batiment.find_all(),
                   'message_contrat_location': 'Une location est déjà en cours à cette période {} au {}'
                  .format(location_courante.date_debut.strftime('%d/%m/%Y'),
                          location_courante.date_fin.strftime('%d/%m/%Y')),
                   'form': form})


def get_assurance(request):
    if request.POST.get('nom_assurance_other'):
        return mdl.assurance.creation_assurance(request.POST.get('nom_assurance_other'))
    else:
        if request.POST['assurance'] and not request.POST['assurance'] == 'None':
            return get_object_or_404(mdl.assurance.Assurance, pk=request.POST['assurance'])
    return None


def get_batiment(batiment_id):
    if batiment_id:
        return mdl.batiment.find_batiment(batiment_id)
    return None


def prolongation(request):
    id_location = request.GET['id_location']
    type_prolongation = request.GET['type_prolongation']
    location = get_object_or_404(mdl.contrat_location.ContratLocation, pk=id_location)
    # response = []
    if location:
        date_trav = location.date_fin
        if date_trav:
            if type_prolongation == "1":
                location.date_fin = date_trav + relativedelta(years=1)
                location.save()
                # response.append('date_fin',location.date_fin)
    # return HttpResponseRedirect(reverse('location-prepare-update-all', args=(id_location,)))
    # return HttpResponse('')
    # return redirect(reverse('location-prepare-update-all', args=(id_location,)))

    # return HttpResponse(simplejson.dumps(response))
    return render(request, "contratlocation_update.html",
                  {'location':    location,
                   'assurances': mdl.assurance.find_all(), })


def contrat_location_form(request):
    nouvelle_location = mdl.contrat_location.ContratLocation()
    auj = date.today()
    nouvelle_location.date_debut = auj.strftime("%d/%m/%Y")
    return render(request, "location/contratlocation_form.html", {
        'assurances': mdl.assurance.find_all(),
        'batiments': mdl.batiment.find_all(),
        'location': nouvelle_location,
        'form': None})


def search(request):
    date_fin = request.GET.get('date_fin_filtre_location', None)
    if date_fin:
        date_fin = datetime.strptime(date_fin, '%d/%m/%Y')
        locations = mdl.contrat_location.search(date_fin)
    else:
        locations = mdl.contrat_location.find_all()
    return render(request, "location/contratlocation_list.html",
                           {'locations': locations,
                            'date_fin_filtre_location': date_fin})
