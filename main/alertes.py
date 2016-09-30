from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main.models import Alerte

from django.shortcuts import render, get_object_or_404


def list(request):
    return render(request, "main/alerte_list.html",
                  {'alertes': Alerte.find_by_etat('A_VERIFIER')})


def update(request, alerte_id):
    alerte = Alerte.objects.get(pk=alerte_id)
    alerte.etat = 'VERIFIER'
    alerte.save()
    return list(request)
