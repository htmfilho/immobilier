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

from main.models import Honoraire
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import datetime
from main.forms import HonoraireForm


def list(request):
    date_limite = timezone.now() - relativedelta(days=15)
    return render(request, "honoraire_list.html",
                  {'honoraires':  Honoraire.find_by_batiment_etat_date(None,'A_VERIFIER', date_limite),
                   'batiments':   Honoraire.find_all_batiments(),
                   'date_limite': date_limite,
                   'etat':        'A_VERIFIER',
                   'batiment':    None})


def search(request):
    batiment_id = None
    if not request.GET['batiment_id'] is None and not request.GET['batiment_id'] == 'TOUS':
        batiment_id = request.GET['batiment_id']

    etat = None
    etat_query = None
    if not request.GET['etat'] is None :
        etat = request.GET['etat']
    if not request.GET['etat'] is None and not request.GET['etat'] == 'TOUS':
        etat_query = request.GET['etat']
    date_limite = None

    if not request.GET.get('date_limite') is None and not request.GET.get('date_limite')== 'None' and not request.GET.get('date_limite')== '':
        date_limite = datetime.strptime(request.GET.get('date_limite'), '%d/%m/%Y')

    return render(request, "honoraire_list.html",
                  {'honoraires':   Honoraire.find_by_batiment_etat_date(batiment_id,etat_query,date_limite),
                   'batiments':    Honoraire.find_all_batiments(),
                   'date_limite':  date_limite,
                   'etat':         etat,
                   'batiment':     batiment_id})


def update(request):
    next_page = request.POST.get('next', None)
    form = HonoraireForm(data=request.POST)
    if 'bt_cancel' not in request.POST:
        if request.POST['honoraire_id'] and not request.POST['honoraire_id'] == 'None':
            honoraire = get_object_or_404(Honoraire, pk=request.POST['honoraire_id'])
        else:
            honoraire = Honoraire()

        honoraire.etat = request.POST['etat']
        if request.POST['date_paiement']:
            try:
                honoraire.date_paiement = datetime.strptime(request.POST['date_paiement'], '%d/%m/%Y')
            except ValueError:
                honoraire.date_paiement = request.POST['date_paiement']
        else:
            honoraire.date_paiement = None
        if form.is_valid():
            honoraire.save()
            if next_page:
                return redirect(next_page)
            else:
                return render(request, "honoraire_list.html", {'honoraires': Honoraire.find_all()})
        else:
            return render(request, "honoraire_form.html", {'honoraire': honoraire,'form': form})
    else:
        return HttpResponseRedirect(reverse('home'))


def honoraire_form(request, honoraire_id):
    next = request.META.get('HTTP_REFERER', '/')
    form = HonoraireForm(data=request.POST)
    a_honoraire = get_object_or_404(Honoraire, pk=honoraire_id)
    return render(request, "honoraire_form.html",
                  {'honoraire': a_honoraire,
                   'form': form,
                   'next': next})
