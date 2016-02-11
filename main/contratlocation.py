from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main.models import Batiment, ContratLocation,Proprietaire, Personne, SuiviLoyer, ContratLocation, Assurance, FinancementLocation
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

def prepare_update(request,location_id):
    location = ContratLocation.objects.get(pk=location_id)
    return render(request, "contratlocation_update.html",
                  {'location': location})


def update(request):
    location = ContratLocation()

    location = get_object_or_404(ContratLocation, pk=request.POST['id'])
    batiment = location.batiment
    if request.POST['renonciation'] :
        location.renonciation = request.POST['renonciation']
    location.remarque = request.POST['remarque']
    print (request.POST['remarque'])
    # assurance  = get_object_or_404(Assurance, pk=request.POST['assurance'])
    # if assurance:
    #     location.assurance = assurance
    location.save()
    location = get_object_or_404(ContratLocation, pk=request.POST['id'])
    print (request.POST['remarque'])
    # return redirect(ContratLocation.objects.all())
    # todo ici il faut retourner au fb
    return render(request, "batiment_form.html",
                  {'batiment': batiment})
    # return redirect('/contratlocations/')


def contratLocation_for_batiment(request, batiment_id):

    batiment = get_object_or_404(Batiment, pk=batiment_id)
    if batiment.location_actuelle:
        location = get_object_or_404(ContratLocation, pk=batiment.location_actuelle.id)
    else:
        location = None
    nouvelle_location = ContratLocation()
    if batiment:
        nouvelle_location.batiment=batiment
    if location:
        nouvelle_location.date_debut=location.date_fin
        nouvelle_location.date_fin=location.date_fin + relativedelta(years=1)
        nouvelle_location.loyer_base=location.loyer_base
        nouvelle_location.charges_base=location.charges_base
    else:
        auj=date.today()
        nouvelle_location.date_debut=auj.strftime("%d/%m/%Y")

        # le financement sera crée automatiquement
    return render(request, "contratlocation_new.html",
                           {'location': nouvelle_location,
                            'nav' : 'list_batiment'})
def list(request):
    locations = ContratLocation.objects.all()
    return render(request, "contratlocation_list.html",
                           {'locations': locations})

def delete(request,location_id):
    location = get_object_or_404(ContratLocation, pk=location_id)
    if location :
        location.delete()
    return render(request, "contratlocation_confirm_delete.html",
                           {'object': location})


def confirm_delete(request):
    location = get_object_or_404(ContratLocation, pk=request.POST['id'])
    location
    return redirect('/contratlocations/')


def test(request):

    batiment = get_object_or_404(Batiment, pk=request.POST['batiment_id'])
    location.batiment = batiment
    location.date_debut = request.POST['date_debut']
    location.date_fin = request.POST['date_fin']

    location.renonciation = request.POST['renonciation']
    location.remarque = request.POST['remarque']
    location.assurance = request.POST['assurance']
    location.loyer_base = request.POST['loyer_base']
    location.charges_base = request.POST['charges_base']
    location.save()

    return redirect('/listeBatiments/')
