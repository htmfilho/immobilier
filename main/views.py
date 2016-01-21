from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main.models import Batiment, ContratLocation,Proprietaire, Personne, SuiviLoyer, ContratGestion, FraisMaintenance
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
from django.views.generic import *
from django.core.urlresolvers import reverse_lazy
from main.forms import PersonneForm, BatimentForm, ProprietaireForm, FraisMaintenanceForm

class ContratGestionList(ListView):
    model = ContratGestion

class ContratGestionDetail(DetailView):
    model = ContratGestion

class FraisMaintenanceList(ListView):
    model = FraisMaintenance

class FraisMaintenanceDetail(DetailView):
    model= FraisMaintenance


# Create your views here.
def dashboard(request):
    return render(request, 'main/dashboard.html', {})

def home(request):
    return render(request, "home.html")

@login_required
def listeBatiments(request):

    batiments = Batiment.objects.all()
    contrats_location = ContratLocation.objects.all()
    return render(request, 'listeBatiments.html', {'batiments': batiments})


def listeProprietaires(request):
    proprietaires = Proprietaire.objects.all()
    return render(request, 'listeProprietaires.html', {'proprietaires': proprietaires})

@login_required
def listePersonnes(request):
    personnes = Personne.objects.all()
    return render(request, 'listePersonnes.html', {'personnes': personnes})

@login_required
def listeComplete(request):
    batiments = Batiment.objects.all()
    contrats_location = ContratLocation.objects.all()
    return render(request, 'listeComplete.html', {'batiments': batiments})

def alertes4(request):
    batiment = Batiment.objects.get(nom='batiment 5b')
    proprietaires = Proprietaire.objects.filter(batiment=batiment)

    return render(request, 'main/alertes4.html', {'batiment' : batiment,'proprietaires': proprietaires})


@login_required
def personne(request, personne_id):
    personne = Personne.find_personne(personne_id)
    return render(request, "personne_form.html",
                  {'personne':         personne})


def update_personne(request):
    print('update_personne')

    personne = Personne()
    print(request.POST['action'])
    if ('add' == request.POST['action'] or 'modify' == request.POST['action']):
        print(request.POST['id'])
        personne = get_object_or_404(Personne, pk=request.POST['id'])
        personne.nom = request.POST['nom']
        personne.prenom = request.POST['prenom']

        personne.save()


    return render(request, "personne_form.html",
                  {'personne':         personne})


def xlsRead(request):
    short_description = u"Export XLS"


class BatimentDetailView(DetailView):
    model = Batiment

    def get_context_data(self, **kwargs):
        context = super(BatimentDetailView, self).get_context_data(**kwargs)
        return context

class FraisMaintenanceDetail(DetailView):
    model= FraisMaintenance

class FraisMaintenanceCreate(CreateView):
    model=FraisMaintenance;
    form_class = FraisMaintenanceForm

class FraisMaintenanceUpdate(UpdateView):
    model=FraisMaintenance;
    form_class = FraisMaintenanceForm

class FraisMaintenanceDelete(DeleteView):
    model=FraisMaintenance;
    success_url = reverse_lazy('fraismaintenance-list'),

class PersonneList(ListView):
    model = Personne

class PersonneDetail(DetailView):
    model= Personne

class PersonneCreate(CreateView):
    model=Personne;
    form_class = PersonneForm

class PersonneUpdate(UpdateView):
    model=Personne;
    form_class = PersonneForm

class PersonneDelete(DeleteView):
    model=Personne;

    success_url="../../../personnes"

class BatimentList(ListView):
    model = Batiment

class BatimentCreate(CreateView):
    model=Batiment;
    form_class = BatimentForm

class BatimentUpdate(UpdateView):
    model=Batiment;
    form_class = BatimentForm

class BatimentDelete(DeleteView):
    model=Batiment;
    success_url="../../../batiments"

class ProprietaireList(ListView):
    model = Proprietaire

class ProprietaireDetail(DetailView):
    model= Proprietaire

class ProprietaireCreate(CreateView):
    model=Proprietaire;
    form_class =ProprietaireForm

class ProprietaireUpdate(UpdateView):
    model=Proprietaire;
    form_class = ProprietaireForm

class ProprietaireDelete(DeleteView):
    model=Proprietaire;

    success_url="../../../proprietaires"
