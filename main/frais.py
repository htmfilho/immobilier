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
    contrat = FraisMaintenance.objects.get(pk=id)
    return render(request, "fraismaintenance_form.html",
                  {'frais': frais,
                   'action' :   'update',
                   'prev': request.GET['prev']})


def update(request):

    if request.POST['action']=='new':
        frais = FraisMaintenance()
        batiment = get_object_or_404(Batiment, pk=request.POST.get('batiment_id',None))
        frais.batiment = batiment
    else:
        frais = get_object_or_404(FraisMaintenance, pk=request.POST.get('id',None))
        batiment = frais.batiment
    personne= None

    if request.POST.get('date_debut',None):
        valid_datetime = datetime.strptime(request.POST['date_debut'], '%d/%m/%Y')
        gestion.date_debut = valid_datetime
    else:
        gestion.date_debut = None

    # gestion.date_fin = request.POST['date_fin']
    if request.POST.get('date_fin',None):
        valid_datetime = datetime.strptime(request.POST['date_fin'], '%d/%m/%Y')
        gestion.date_fin = valid_datetime
    else:
        gestion.date_fin =None
    if gestion.date_debut and gestion.date_fin :
        if gestion.date_debut> gestion.date_fin :
            return render(request, "contratgestion_update.html",
                          {'contrat': gestion,
                           'message':'La date de début doit être < à la date de fin'})
    message
    if not message is None:

        return render(request, "fraismaintenance_form.html",
                      {'frais': frais,
                       'action' :   'update',
                       'message' : message,
                       'prev': request.GET['prev']})


    frais.save()
    if request.POST.get('prev', None) == 'fb':
        return render(request, "batiment_form.html",
                      {'batiment': batiment})



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
