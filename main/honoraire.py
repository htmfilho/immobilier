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
from main.forms import HonoraireForm

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
    batiment_id = request.GET['batiment_id']
    batiment_id =None
    if not request.GET['batiment_id'] is None and not request.GET['batiment_id'] == 'TOUS':
        batiment_id = request.GET['batiment_id']

    etat = None
    etat_query = None
    if not request.GET['etat'] is None :
        etat = request.GET['etat']
    if not request.GET['etat'] is None and not request.GET['etat'] == 'TOUS':
        etat_query = request.GET['etat']
    print(etat)
    date_limite = None

    if not request.GET.get('date_limite') is None and not request.GET.get('date_limite')== 'None' and not request.GET.get('date_limite')== '':
        date_limite = datetime.strptime(request.GET.get('date_limite'), '%d/%m/%Y')

    return render(request, "honoraire_list.html",
                  {'honoraires':   Honoraire.find_by_batiment_etat_date(batiment_id,etat_query,date_limite),
                   'batiments' :   Honoraire.find_all_batiments(),
                   'date_limite' : date_limite,
                   'etat':         etat,
                   'batiment'  :   batiment_id})


def update(request):

    form = HonoraireForm(data=request.POST)
    if request.POST['honoraire_id'] and not request.POST['honoraire_id'] == 'None':
        honoraire = get_object_or_404(Honoraire, pk=request.POST['honoraire_id'])

    else:
        honoraire = Honoraire()

    honoraire.etat = request.POST['etat']
    if request.POST['date_paiement']:
        try:
            honoraire.date_paiement =datetime.strptime(request.POST['date_paiement'], '%d/%m/%Y')
        except ValueError:
            honoraire.date_paiement =request.POST['date_paiement']
    else:
        honoraire.date_paiement =None
    if form.is_valid():
        honoraire.save()
        return render(request, "honoraire_list.html",
                      {'honoraires': Honoraire.find_all()})
    else:
        return render(request, "honoraire_form.html",
                      {'honoraire': honoraire,'form': form})

def honoraire_form(request, honoraire_id):
    form = HonoraireForm(data=request.POST)
    honoraire = get_object_or_404(Honoraire, pk=honoraire_id)
    return render(request, "honoraire_form.html",
                  {'honoraire': honoraire,
                   'form': form})
