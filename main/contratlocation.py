from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main.models import*
from django.views.generic import DetailView
from django.core.urlresolvers import reverse
import os
from .exportUtils import export_xls_batiment
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import date
import datetime
from django.db import models
from datetime import datetime
from main.forms import ContratLocationForm
from dateutil.relativedelta import relativedelta
from django.http import HttpRequest


def prepare_update(request, location_id):
    location = ContratLocation.objects.get(pk=location_id)
    return render(request, "contratlocation_update.html",
                  {'location':    location,
                   'assurances': Assurance.find_all(), })


def update(request):
    print('update')
    previous = request.POST.get('previous', None)
    id = request.POST.get('id', None)
    form = ContratLocationForm(data=request.POST)
    location = get_object_or_404(ContratLocation, pk=id)

    if request.POST['renonciation']:
        location.renonciation = datetime.strptime(request.POST['renonciation'], '%d/%m/%Y')
    location.remarque = request.POST['remarque']

    if request.POST['assurance'] and not request.POST['assurance'] == '-':
        location.assurance = get_object_or_404(Assurance, pk=request.POST['assurance'])
    else:
        location.assurance = None

    if form.is_valid():

        print('form is valid')

        location.save()
        # todo ici il faut retourner au fb
        return redirect(previous)
        # return redirect('/contratlocations/')
    else:
        print(form.errors)
        print('form is not valid')
        return render(request, "contratlocation_update.html",
                               {'location':    location,
                                'assurances':  Assurance.find_all(),
                                'nav':         'list_batiment',
                                'form':        form})


def contrat_location_for_batiment(request, batiment_id):

    batiment = get_object_or_404(Batiment, pk=batiment_id)
    if batiment.location_actuelle:
        location = get_object_or_404(ContratLocation, pk=batiment.location_actuelle.id)
    else:
        location = None
    nouvelle_location = ContratLocation()
    if batiment:
        nouvelle_location.batiment = batiment
    if location is not None:
        nouvelle_location.date_debut = location.date_fin
        nouvelle_location.date_fin = location.date_fin + relativedelta(years=1)
        nouvelle_location.loyer_base = location.loyer_base
        nouvelle_location.charges_base = location.charges_base
    else:
        auj=date.today()
        nouvelle_location.date_debut = auj.strftime("%d/%m/%Y")

        # le financement sera crée automatiquement
    print('11')
    return render(request, "contratlocation_new.html",
                           {'location': nouvelle_location,
                            'assurances': Assurance.find_all(),
                            'nav': 'list_batiment'})


def list(request):
    locations = ContratLocation.objects.all()
    return render(request, "contratlocation_list.html",
                           {'locations': locations})


def delete(request,location_id):
    location = get_object_or_404(ContratLocation, pk=location_id)
    if location:
        location.delete()
    return render(request, "contratlocation_confirm_delete.html",
                           {'object': location})


def confirm_delete(request):
    location = get_object_or_404(ContratLocation, pk=request.POST['id'])
    return redirect('/contratlocations/')


def test(request):
    print('test')
    """
    ok - 1
    """
    form = ContratLocationForm(data=request.POST)

    batiment = get_object_or_404(Batiment, pk=request.POST['batiment_id'])
    location = ContratLocation()
    location.batiment = batiment
    if request.POST['date_debut']:
        location.date_debut = datetime.strptime(request.POST['date_debut'], '%d/%m/%Y')
        location.date_fin =location.date_debut + relativedelta(years=1)
        location.renonciation =location.date_debut + relativedelta(days=355)
    else:
        location.date_debut = None
    # if request.POST.get('date_fin'):
    #     location.date_fin = datetime.strptime(request.POST['date_fin'], '%d/%m/%Y')
    # else:
    #     location.date_fin = None
    print('dd :',location.date_fin)
    # if request.POST.get('renonciation'):
    #     location.renonciation = request.POST['renonciation']
    # else:
    #     location.renonciation = None
    location.remarque = request.POST['remarque']
    if request.POST.get('nom_assurance_other'):
        assurance = Assurance()
        assurance.nom = request.POST.get('nom_assurance_other')
        assurance.save()
        location.assurance = assurance
    else:
        if request.POST['assurance'] and not request.POST['assurance'] == 'None':
            location.assurance = get_object_or_404(Assurance, pk=request.POST['assurance'])
        else:
            location.assurance = None

    location.loyer_base = request.POST['loyer_base']
    location.charges_base = request.POST['charges_base']

    if form.is_valid():
        print('form valid')
        location.save()
    else:
        print('form invalid', form.errors)
        print('1')
        return render(request, "contratlocation_new.html",
                               {'location':    location,
                                'assurances': Assurance.find_all(),
                                'nav':       'list_batiment',
                                'form': form})

    if request.POST.get('prev', None) == 'fb':
        return render(request, "batiment_form.html",
                      {'batiment': batiment})


    lnk = None
    if request.POST.get('return_lnk'):
        print(request.POST.get('return_lnk'))
        lnk = request.POST.get('return_lnk')
    print(lnk)

    if lnk:
        return redirect(lnk)
    else:
        return redirect('/listeBatiments/')
