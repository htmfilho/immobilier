from main.models import Societe

from django.shortcuts import render


def societe_liste(request):
    print('societe_liste')
    return render(request, 'liste_societes.html', {'societes': Societe.find_all()})
