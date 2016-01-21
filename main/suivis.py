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

def suivis_search(request):

    date_debut = request.GET['date_debut']
    date_fin = request.GET['date_fin']
    etat = request.GET['etat']


    print (date_debut)

    suivis = SuiviLoyer.find_suivis(date_debut,date_fin, etat)

    return render(request, "suivis.html",
                  {'date_debut':date_debut,
                  'date_fin':date_fin,
                  'etat':etat,
                   'suivis':           suivis
                  })


def suivis(request):
    print (timezone.now().strftime('%d-%m-%Y') )
    return render(request, "suivis.html",
                  {'date_debut':       timezone.now(),
                   'date_fin':         timezone.now() + relativedelta(months=1),
                   'suivis':           None
                  })


def refresh_suivis(request):
    print('refresh_suivis')
    date_debut = request.POST['date_debut']
    date_fin = request.POST['date_fin']
    etat =  request.POST['etat']
    if etat == "TOUS":
        etat = None
    # print(date_debut.strftime('%Y-%m-%d'))
    suivis = SuiviLoyer.find_suivis(date_debut,date_fin, etat)

    return render(request, "suivis.html",
                  {'date_debut':       date_debut,
                   'date_fin':         date_fin,
                   'suivis':           suivis
                  })
