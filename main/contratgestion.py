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
    """
    ok - 1
    """
    batiment = get_object_or_404(Batiment, pk=batiment_id)
    contrat = ContratGestion()
    contrat.batiment= batiment
    # Par défaut Sté comme gestionnaire

    personne_gestionnaire = Personne.find_gestionnaire_default()
    if personne_gestionnaire:
        contrat.gestionnaire = personne_gestionnaire
    return render(request, "contratgestion_update.html",
                  {'contrat':   contrat,
                   'personnes': Personne.find_all(),
                   'action' :   'new',
                   'prev':      'fb'})

def prepare_update(request,id):
    contrat = ContratGestion.objects.get(pk=id)
    return render(request, "contratgestion_update.html",
                  {'contrat': contrat,
                   'action' :   'update',
                   'prev': request.GET['prev']})


def update(request):
    """
    ok - 1
    """
    if request.POST['action']=='new':
        gestion = ContratGestion()
        batiment = get_object_or_404(Batiment, pk=request.POST.get('batiment_id',None))
        gestion.batiment = batiment
    else:
        gestion = get_object_or_404(ContratGestion, pk=request.POST.get('id',None))
        batiment = gestion.batiment
    personne= None
    if request.POST.get('gestionnaire',None):
        personne = get_object_or_404(Personne, pk=request.POST.get('gestionnaire',None))
        gestion.gestionnaire = personne

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
    if personne is None:
        message = "Il faut sélectionner un gestionnaire"
        return render(request, "contratgestion_update.html",
                      {'contrat': contrat,
                       'action' :   'update',
                       'message' : message,
                       'prev': request.GET['prev']})


    gestion.save()
    if request.POST.get('prev', None) == 'fb':
        return render(request, "batiment_form.html",
                      {'batiment': batiment})



    return redirect('/contratgestions/')

def list(request):
    contrats = ContratGestion.objects.all()
    return render(request, "contratgestion_list.html",
                           {'contrats': contrats})

def delete(request,contrat_gestion_id):
    contrat_gestion = get_object_or_404(ContratGestion, pk=contrat_gestion_id)
    batiment = contrat_gestion.batiment
    if contrat_gestion :
        contrat_gestion.delete()
    return render(request, "batiment_form.html",
                  {'batiment': batiment})
