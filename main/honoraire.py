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
import datetime
from django.db import models
from datetime import datetime

def list(request):
    date_limite = timezone.now() - relativedelta(days=15)
    # proprietaire.date_debut = datetime.strptime(request.POST['date_debut'], '%d/%m/%Y')
    return render(request, "honoraire_list.html",
                  {'honoraires':   Honoraire.find_by_batiment_etat_date(None,'A_VERIFIER',date_limite),
                   'batiments' :   Honoraire.find_all_batiments(),
                   'date_limite' : date_limite,
                   'etat' :        'A_VERIFIER',
                   'batiment'  :   None})

def search(request):
    print('search')
    batiment_id = request.GET['batiment_id']
    print( batiment_id)
    batiment_id =None
    if not request.GET['batiment_id'] is None and not request.GET['batiment_id'] == 'TOUS':
        batiment_id = request.GET['batiment_id']

    etat = None
    if not request.GET['etat'] is None and not request.GET['etat'] == 'TOUS':
        etat = request.GET['etat']

    date_limite = None
    if not request.GET['date_limite'] is None and not request.GET['date_limite']== 'None':
        date_limite = datetime.strptime(request.GET['date_limite'], '%d/%m/%Y')

    return render(request, "honoraire_list.html",
                  {'honoraires':   Honoraire.find_by_batiment_etat_date(batiment_id,etat,date_limite),
                   'batiments' :   Honoraire.find_all_batiments(),
                   'date_limite' : date_limite,
                   'etat':         etat,
                   'batiment'  :   batiment_id})
