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
from django.template import loader
from datetime import datetime
from . import batiment

def listeProprietaires(request):
    proprietaires = Proprietaire.objects.all()
    return render(request, 'listeProprietaires.html', {'proprietaires': proprietaires})

def proprietaire(request, proprietaire_id):
    proprietaire = Proprietaire.find_proprietaire(proprietaire_id)
    return render(request, "proprietaire_form.html",
                  {'proprietaire':         proprietaire,
                   'action':               'update',
                   'personnes':            Personne.objects.all(),
                   'prev' : request.GET.get('prev')})

def add_proprietaire(request, batiment_id):
    """
    Ajoute un propriétaire à un batiment existantes
    ok - 1
    """
    batiment = get_object_or_404(Batiment, pk=batiment_id)
    proprietaire = Proprietaire()
    proprietaire.batiment = batiment
    return render(request, "proprietaire_form.html",
                  {'proprietaire': proprietaire,
                   'action':       'add',
                   'personnes':    Personne.objects.all()})

def update_proprietaire(request, proprietaire_id):
    proprietaire = Proprietaire.find_proprietaire(proprietaire_id)
    return render(request, "proprietaire_form.html",
                  {'proprietaire':         proprietaire,
                   'action':               'update',})


def delete_proprietaire_batiment(request, proprietaire_id):
    print('delete_proprietaire_batiment')
    proprietaire = Proprietaire.find_proprietaire(proprietaire_id)
    batiment =  proprietaire.batiment
    proprietaire.delete()

    return render(request, "batiment_form.html",
                  {'batiment': batiment})

def delete_proprietaire(request, proprietaire_id):
    proprietaire = Proprietaire.find_proprietaire(proprietaire_id)
    batiment =  proprietaire.batiment
    proprietaire.delete()
    print(request)
    # if '/p/' in request.get_full_path():
    #     print('if')
    #     return render(request, "proprietaire_form.html",
    #                   {'proprietaire':         proprietaire})
    # if '/pl/' in request.get_full_path():
    #     return  listeProprietaires

    if not request.POST.get('prev', None) is None:
        return redirections(request, batiment)

    return render(request, "proprietaire_form.html",
                  {'proprietaire':         proprietaire})


def proprietaire_update_save(request):
    print('proprietaire_update_save',request.POST['prev'],None)
    if 'update' == request.POST['action']:
        proprietaire = get_object_or_404(Proprietaire, pk=request.POST['id'])
    if 'add' == request.POST['action']:
        proprietaire=Proprietaire()

    if request.POST['date_debut']:
        proprietaire.date_debut = datetime.strptime(request.POST['date_debut'], '%d/%m/%Y')
    if request.POST['date_fin']:
        proprietaire.date_fin = datetime.strptime(request.POST['date_fin'], '%d/%m/%Y')


    personne = get_object_or_404(Personne, pk=request.POST['proprietaire'])
    proprietaire.proprietaire = personne
    if 'add' == request.POST['action']:
        batiment = get_object_or_404(Batiment, pk=request.POST['batiment_id'])
        proprietaire.batiment = batiment
    if not proprietaire.date_debut is None and not proprietaire.date_fin is None:
        if proprietaire.date_debut> proprietaire.date_fin :
            return render(request, "proprietaire_form.html",
                          {'proprietaire': proprietaire,
                           'message':'La date de début doit être < à la date de fin'})
    proprietaire.save()
    if 'add' == request.POST['action']:
        batiments = Batiment.objects.all()
        return render(request, 'listeBatiments.html', {'batiments': batiments})
    if not request.POST['prev'] is None:
        return redirections(request, proprietaire.batiment)

def redirections(request,batiment):
    print('redirection',request.POST.get('prev', None))
    if request.POST.get('prev', None) == 'lp':
        return listeProprietaires(request)
    if request.POST.get('prev', None) == 'fb':
        return render(request, "batiment_form.html",
                      {'batiment': batiment})

def proprietaire_create_for_batiment(request, batiment_id):
    batiment = get_object_or_404(Batiment, pk=batiment_id)
    proprietaire=Proprietaire()
    if batiment:
        proprietaire.batiment=batiment
    personnes =  Personne.objects.all()

    return render(request, "proprietaire_form.html",
                  {'proprietaire':         proprietaire,
                   'personnes':            personnes,
                   'action':               'add'})


def personne_create(request):
    print('personne_create')
    proprietaire = get_object_or_404(Proprietaire, pk=request.POST['proprietaire_id_pers'])
    print(proprietaire)
    personne = Personne()
    personne.nom =request.POST['nom']
    personne.prenom =request.POST['prenom']
    personne.save()
    print(personne)
    proprietaire.personne=personne
    personnes = Personne.objects.filter()

    return render(request, "proprietaire_form.html",
                  {'proprietaire': proprietaire,
                   'personnes': personnes})
