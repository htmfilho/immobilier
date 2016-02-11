from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main.models import Alerte
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

def list(request):
    return render(request, "main/alerte_list.html",
                  {'alertes': Alerte.find_by_etat('A_VERIFIER')})


def update(request, alerte_id):
    alerte = Alerte.objects.get(pk=alerte_id)
    alerte.etat = 'VERIFIER'
    alerte.save()
    return list(request)
