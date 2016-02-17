from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main.models import *
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

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main.models import *
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
import locale

def new(request):
    frais = FraisMaintenance()

    return render(request, "fraismaintenance_form.html",
                  {'frais':   frais,
                   'personnes': Personne.find_all(),
                   'action' :   'new',
                   'batiments' : Batiment.find_all(),
                   'prev':      'fl'})

def create(request, batiment_id):

    batiment = get_object_or_404(Batiment, pk=batiment_id)
    frais = FraisMaintenance()
    frais.batiment= batiment

    return render(request, "fraismaintenance_form.html",
                  {'frais':   frais,
                   'personnes': Personne.find_all(),
                   'action' :   'new',
                   'prev':      'fb'})

def prepare_update(request,id):
    frais = FraisMaintenance.objects.get(pk=id)
    return render(request, "fraismaintenance_form.html",
                  {'frais':   frais,
                   'action' : 'update',
                   'prev':    'fl'})


def update(request):
    print('update',request.POST['action'])
    if request.POST['action']=='new':
        frais = FraisMaintenance()
        batiment = get_object_or_404(Batiment, pk=request.POST.get('batiment_id',None))
        frais.batiment = batiment
    else:
        frais = get_object_or_404(FraisMaintenance, pk=request.POST.get('id',None))
        batiment = frais.batiment
    personne= None

    if request.POST.get('entrepreneur',None):
        frais.entrepreneur = request.POST['entrepreneur']
    else:
        frais.entrepreneur = None
    if request.POST.get('societe',None):
        frais.societe = request.POST['societe']
    else:
        frais.societe = None
    if request.POST.get('description',None):
        frais.description = request.POST['description']
    else:
        frais.description = None

    if request.POST.get('montant',None):
        frais.montant = request.POST['montant']
    else:
        frais.montant = None
    if request.POST.get('date_realisation',None):
        valid_datetime = datetime.strptime(request.POST['date_realisation'], '%d/%m/%Y')
        frais.date_realisation = valid_datetime
    else:
        frais.date_realisation = None

    frais.save()
    if request.POST.get('prev', None) == 'fb':
        return render(request, "batiment_form.html",
                      {'batiment': batiment})
    if request.POST.get('prev', None) == 'fl':
        return render(request, "fraismaintenance_list.html",
                               {'frais_list': FraisMaintenance.objects.all()})



    return redirect('/fraismaintenances/')

def list(request):
    frais_list = FraisMaintenance.objects.all()
    return render(request, "fraismaintenance_list.html",
                           {'frais_list': frais_list})

def delete(request,id):
    frais = get_object_or_404(FraisMaintenance, pk=id)
    batiment = frais.batiment
    if frais :
        frais.delete()
    return render(request, "batiment_form.html",
                  {'batiment': batiment})
