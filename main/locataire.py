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

def locataire_form(request, id):
    locataire = get_object_or_404(Locataire, pk=id)
    return render(request, "locataire_form.html",
                  {'locataire' : locataire,
                   'action' : 'update',
                   'personnes' : Personne.find_all() })

def update(request, id):
    print(update)
    locataire = get_object_or_404(Locataire, pk=id)
    return render(request, "locataire_form.html",
                  {'locataire':         locataire})

def new(request, location_id):
    print(new)
    print('new locataire', location_id)
    location = get_object_or_404(ContratLocation, pk=location_id)

    locataire = Locataire()
    locataire.contrat_location=location
    personnes = Personne.objects.filter()
    l=[]
    if personnes:
        for p in personnes:
            l.append(p)

        for loca in location.locataires:
            l.remove(loca.personne)

    return render(request, "locataire_form.html",
                  {'locataire': locataire,
                   'location' : location,
                   'personnes': l})

def add(request):
    print('add')
    if request.POST['locataire_id'] and not request.POST['locataire_id']== 'None':
        locataire = get_object_or_404(Locataire, pk=request.POST.get('locataire_id',None))
    else:
        locataire = Locataire()

    location = get_object_or_404(ContratLocation, pk=request.POST.get('location_id',None))
    if request.POST['personne_id']:
        personne = get_object_or_404(Personne, pk=request.POST['personne_id'])
        locataire.personne = personne

    locataire.principal = False
    if request.POST.get('principal',None) and request.POST['principal'] == 'on':
        locataire.principal = True
    locataire.civilite = request.POST['civilite']
    locataire.infos_complement = request.POST['infos_complement']
    locataire.societe = request.POST['societe']
    locataire.tva = request.POST['tva']
    locataire.profession = request.POST['profession']
    locataire.contrat_location = location
    locataire.save()
    return render(request, "contratlocation_update.html",
                  {'location': location})

def delete(request,locataire_id):
    locataire = get_object_or_404(Locataire, pk=locataire_id)
    location = locataire.contrat_location
    locataire.delete()
    return render(request, "contratlocation_update.html",
                  {'location': location})


def personne_create(request):
    location = get_object_or_404(ContratLocation, pk=request.POST['location_id_pers'])
    locataire = Locataire()
    locataire.contrat_location=location


    personne = Personne()
    personne.nom =request.POST['nom']
    personne.prenom =request.POST['prenom']
    personne.save()
    locataire.personne=personne
    personnes = Personne.objects.filter()

    return render(request, "locataire_form.html",
                  {'locataire': locataire,
                   'location' : location,
                   'personnes': personnes})


def list(request):
    return render(request, "locataire_list.html",
                  {'locataires': Locataire.objects.all(),
                   'personnes': Personne.find_all()})
