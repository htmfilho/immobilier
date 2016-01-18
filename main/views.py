from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main.models import Batiment, ContratLocation,Proprietaire, Personne
from django.views.generic import DetailView
import os
from .exportUtils import export_xls_batiment


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
    
@login_required
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
def batiment(request, batiment_id):
    batiment = Batiment.find_batiment(batiment_id)
    return render(request, "batiment.html",
                  {'batiment':         batiment}) 
                  
@login_required 
def proprietaire(request, proprietaire_id):
    proprietaire = Proprietaire.find_proprietaire(proprietaire_id)
    return render(request, "proprietaire.html",
                  {'proprietaire':         proprietaire}) 

@login_required 
def personne(request, personne_id):
    personne = Personne.find_personne(personne_id)
    return render(request, "personne.html",
                  {'personne':         personne})                 

def xlsRead(request):
    short_description = u"Export XLS"
    

class BatimentDetailView(DetailView):    
    model = Batiment

    def get_context_data(self, **kwargs):
        context = super(BatimentDetailView, self).get_context_data(**kwargs)
        return context