from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main.models import *
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
                  {'batiment':         batiment,
                   'localites':    Localite.find_all()})

def batiment_form(request, batiment_id):
    print('batiment_form')
    batiment = Batiment.find_batiment(batiment_id)

    return render(request, "batiment_form.html",
                  {'batiment':     batiment,
                   'assurances':   Assurance.find_all(),
                   'localites':    Localite.find_all()})

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
        localite = None
        if request.POST['localite']:
            localite = get_object_or_404(Localite, pk=request.POST['localite'])

        batiment.localite = localite
        print(request.POST['superficie'])
        if request.POST['superficie']:
            batiment.superficie = request.POST['superficie']
        else:
            batiment.superficie = None
        if request.POST['peformance_energetique']:
            batiment.peformance_energetique = request.POST['peformance_energetique']
        else:
            batiment.peformance_energetique = None
        batiment.save()


    return render(request, "batiment_form.html",
                  {'batiment':     batiment,
                   'localites':    Localite.find_all()})
