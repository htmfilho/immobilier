##############################################################################
#
#    Immobilier it's an application
#    designed to manage the core business of property management, buildings,
#    rental agreement and so on.
#
#    Copyright (C) 2016-2017 Verpoorten Leïla
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import datetime
from main.forms import HonoraireForm
from main import models as mdl
from main.models.enums import etat_honoraire
from main import views_utils


DEFAULT_ETAT_LIST = etat_honoraire.A_VERIFIER
DATE_LIMITE_INFERIEURE_FILTRE_DEFAUT = timezone.now() - relativedelta(days=15)
DATE_LIMITE_SUPERIEURE_FILTRE_DEFAUT = timezone.now() + relativedelta(days=15)


def list(request):

    return render(request, "honoraire/honoraire_list.html",
                  {'honoraires':  mdl.honoraire.find_by_batiment_etat_date(None,
                                                                           DEFAULT_ETAT_LIST,
                                                                           DATE_LIMITE_INFERIEURE_FILTRE_DEFAUT,
                                                                           DATE_LIMITE_SUPERIEURE_FILTRE_DEFAUT),
                   'batiments':   mdl.honoraire.find_all_batiments(),
                   'DATE_LIMITE_INFERIEURE_FILTRE_DEFAUT': DATE_LIMITE_INFERIEURE_FILTRE_DEFAUT,
                   'DATE_LIMITE_SUPERIEURE_FILTRE_DEFAUT': DATE_LIMITE_SUPERIEURE_FILTRE_DEFAUT,
                   'etat': 'A_VERIFIER',
                   'batiment': None})


def search(request):
    batiment_id = None
    if not request.GET['batiment_id'] is None and not request.GET['batiment_id'] == 'TOUS':
        batiment_id = int(request.GET['batiment_id'])

    etat = None
    etat_query = None
    if not request.GET['etat'] is None:
        etat = request.GET['etat']
    if not request.GET['etat'] is None and not request.GET['etat'] == 'TOUS':
        etat_query = request.GET['etat']
    date_limite = get_date(request, 'date_limite')
    date_limite_sup = get_date(request, 'date_limite_sup')

    batiment_selected = batiment_id
    if batiment_selected is None:
        batiment_selected = "TOUS"
    return render(request, "honoraire/honoraire_list.html",
                  {'honoraires': mdl.honoraire.find_by_batiment_etat_date(batiment_id,
                                                                          etat_query,
                                                                          date_limite,
                                                                          date_limite_sup),
                   'batiments': mdl.honoraire.find_all_batiments(),
                   'date_limite': date_limite,
                   'date_limite_sup': date_limite_sup,
                   'etat': etat,
                   'batiment': batiment_selected})


def get_date(request, nom_parametre):
    date_limite = None

    if not request.GET.get(nom_parametre) is None and not request.GET.get(nom_parametre) == 'None' \
            and not request.GET.get(nom_parametre) == '':
        date_limite = datetime.strptime(request.GET.get(nom_parametre), '%d/%m/%Y')
    return date_limite


def update(request):
    next_page = request.POST.get('next', None)
    form = HonoraireForm(data=request.POST)

    honoraire_maj = get_honoraire(request)
    honoraire_maj.etat = request.POST['etat']

    honoraire_maj.date_paiement = views_utils.get_date(request.POST.get('date_paiement', None))

    if form.is_valid():
        honoraire_maj.save()
        if next_page:
            return redirect(next_page)
        else:
            return render(request, "honoraire_maj/honoraire_list.html", {'honoraires': mdl.honoraire.find_all()})
    else:
        return render(request, "honoraire_maj/honoraire_form.html", {'honoraire_maj': honoraire_maj, 'form': form})



def get_honoraire(request):
    if request.POST['honoraire_id'] and not request.POST['honoraire_id'] == 'None':
        honoraire = get_object_or_404(mdl.honoraire.Honoraire, pk=request.POST['honoraire_id'])
    else:
        honoraire = mdl.honoraire.Honoraire()
    return honoraire


def honoraire_form(request, honoraire_id):
    next = request.META.get('HTTP_REFERER', '/')
    form = HonoraireForm(data=request.POST)
    a_honoraire = get_object_or_404(mdl.honoraire.Honoraire, pk=honoraire_id)
    return render(request, "honoraire/honoraire_form.html",
                  {'honoraire': a_honoraire,
                   'form': form,
                   'next': next})
