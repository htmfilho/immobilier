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


def proprietaire(request, proprietaire_id):
    proprietaire = Proprietaire.find_proprietaire(proprietaire_id)
    return render(request, "proprietaire_form.html",
                  {'proprietaire':         proprietaire})

def add_proprietaire(request, batiment_id):
    proprietaire = Proprietaire.find_proprietaire(proprietaire_id)
    return render(request, "proprietaire_form.html",
                  {'proprietaire':         proprietaire})

def update_proprietaire(request, proprietaire_id):
    proprietaire = Proprietaire.find_proprietaire(proprietaire_id)
    return render(request, "proprietaire_form.html",
                  {'proprietaire':         proprietaire})


def delete_proprietaire(request, proprietaire_id):
    proprietaire = Proprietaire.find_proprietaire(proprietaire_id)
    return render(request, "proprietaire_form.html",
                  {'proprietaire':         proprietaire})
