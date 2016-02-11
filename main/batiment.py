from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main.models import Batiment, ContratLocation,Proprietaire, Personne, SuiviLoyer
from django.views.generic import DetailView
from django.core.urlresolvers import reverse
import os
from .exportUtils import export_xls_batiment
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import datetime
from django.db import models

def create(request):
    batiment = Batiment()
    return render(request, "batiment_form.html",
                  {'batiment':         batiment})

def batiment_form(request, batiment_id):
    batiment = Batiment.find_batiment(batiment_id)
    return render(request, "batiment_form.html",
                  {'batiment':         batiment})

def update(request):

    batiment = Batiment()

    if ('add' == request.POST['action'] or 'modify' == request.POST['action']):
        if request.POST['id'] and not request.POST['id'] == 'None':
            batiment = get_object_or_404(Batiment, pk=request.POST['id'])
        else:
            batiment = Batiment()
        batiment.rue = request.POST['rue']
        print(request.POST['numero'])
        batiment.numero = request.POST['numero']
        batiment.boite = request.POST['boite']
        batiment.code_postal = request.POST['code_postal']
        batiment.localite = request.POST['localite']

        batiment.save()


    return render(request, "batiment_form.html",
                  {'batiment':         batiment})
