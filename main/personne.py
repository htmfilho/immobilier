from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main.models import ContratLocation,Proprietaire, Personne, ContratLocation, Locataire

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
from main.forms import PersonneForm


def edit(request, personne_id):
    if personne_id:
        personne = Personne.find_personne(personne_id)
    else:
        personne = Personne()
    return render(request, "personne_form.html",
                  {'personne': personne})

def create(request):
    return render(request, "personne_form.html",
                  {'personne': Personne()})

def list(request):
    return render(request, "personne_list.html",
                  {'personnes': Personne.find_all()})

def update(request):

    form = PersonneForm(data=request.POST)
    if request.POST['personne_id'] and not request.POST['personne_id'] == 'None':
        personne = get_object_or_404(Personne, pk=request.POST['personne_id'])

    else:
        personne = Personne()

    personne.nom =request.POST['nom']
    personne.prenom =request.POST['prenom']
    personne.email =request.POST['email']
    personne.profession =request.POST['profession']

    personne.lieu_naissance =request.POST['lieu_naissance']
    personne.pays_naissance =request.POST['pays_naissance']
    personne.num_identite =request.POST['num_identite']
    personne.telephone =request.POST['telephone']
    personne.gsm =request.POST['gsm']
    if request.POST['date_naissance']:
        try:
            personne.date_naissance =datetime.strptime(request.POST['date_naissance'], '%d/%m/%Y')
        except ValueError:
            personne.date_naissance =request.POST['date_naissance']
    else:
        personne.date_naissance =None
    if form.is_valid():
        personne.save()
        return render(request, "personne_list.html",
                      {'personnes': Personne.find_all()})
    else:
        return render(request, "personne_form.html",
                      {'personne': personne,'form': form})
