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
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import datetime
from main.forms import SuiviForm
from django.shortcuts import redirect
from main import models as mdl


def suivis_search(request):
    date_debut = request.GET['date_debut']
    date_fin = request.GET['date_fin']
    etat = request.GET['etat']

    if date_debut:
        date_debut = datetime.strptime(request.GET['date_debut'], '%d/%m/%Y')
    if date_fin:
        date_fin = datetime.strptime(request.GET['date_fin'], '%d/%m/%Y')
    if etat == 'TOUS':
        etat = None
    return list_suivis(request, date_debut, date_fin, etat)


def list_suivis(request, date_debut, date_fin, etat):
    if etat is None:
        etat = 'TOUS'
    return render(request, "suivi/suivis.html",
                  {'date_debut': date_debut,
                   'date_fin':    date_fin,
                   'etat':        etat,
                   'suivis':      mdl.suivi_loyer.find_suivis(date_debut, date_fin, etat)})


def suivis(request):
    date_fin = timezone.now() - relativedelta(days=1)
    return render(request, "suivi/suivis.html",
                  {'date_debut':       None,
                   'date_fin':         date_fin,
                   'suivis':           mdl.suivi_loyer.find_suivis(None, date_fin, None)
                   })


def refresh_suivis(request):
    print('refresh_suivis')
    date_debut = request.POST['date_debut']
    date_fin = request.POST['date_fin']
    etat = request.POST['etat']
    if etat == "TOUS":
        etat = None
    # print(date_debut.strftime('%Y-%m-%d'))
    return render(request, "suivi/suivis.html",
                  {'date_debut':       date_debut,
                   'date_fin':         date_fin,
                   'suivis':           mdl.suivi_loyer.find_suivis(date_debut, date_fin, etat)
                   })


def suivis_update(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        for key, value in request.POST.iteritems():
            print(key, value)
            if key.startswith('suivi_'):
                print('info suivis')

        pass

    date_debut = request.POST['date_debut']
    date_fin = request.POST['date_fin']
    etat = request.POST['etat']
    if etat == "TOUS":
        etat = None
    # print(date_debut.strftime('%Y-%m-%d'))

    return render(request, "suivi/suivis.html",
                  {'date_debut':       date_debut,
                   'date_fin':         date_fin,
                   'suivis':           mdl.suivi_loyer.find_suivis(date_debut, date_fin, etat)
                   })


def suivis_updatel(request, suivi_id):
    print('suivis_updatel')
    suivi = get_object_or_404(mdl.suivi_loyer.SuiviLoyer, pk=suivi_id)
    # etat =  request.POST['etat']
    # print (etat)
    etat = request.GET['etat']
    date_debut = request.GET['dated']
    date_fin = request.GET['datef']
    if date_debut:
        date_debut = datetime.strptime(date_debut, '%d/%m/%Y')
    if date_fin:
        date_fin = datetime.strptime(date_fin, '%d/%m/%Y')

    # etat = request.GET['etat']
    return render(request, "suivi/suivi_form.html",
                  {'suivi':      suivi,
                   'date_debut': date_debut,
                   'date_fin':   date_fin,
                   'etat':       etat})


def update_suivi(request):
    print('update_suivi')
    etat = request.POST['etat']
    suivi = get_object_or_404(mdl.suivi_loyer.SuiviLoyer, pk=request.POST['id'])

    if request.POST.get('date_paiement_reel', None):
        suivi.date_paiement_reel = datetime.strptime(request.POST['date_paiement_reel'], '%d/%m/%Y')
    else:
        suivi.date_paiement_reel = None
    print(request.POST['etat_suivi'])
    if request.POST['etat_suivi']:
        if request.POST['etat_suivi'] == '-' or request.POST['etat_suivi'] == 'TOUS':
            suivi.etat_suivi = None
        else:
            suivi.etat_suivi = request.POST['etat_suivi']
    else:
        suivi.etat_suivi = 'A_VERIFIER'

    if request.POST['loyer_percu']:
        suivi.loyer_percu = request.POST['loyer_percu']
    else:
        suivi.loyer_percu = 0

    if request.POST.get('charges_percu', None):
        suivi.charges_percu = request.POST['charges_percu']
    else:
        suivi.charges_percu = 0

    if request.POST['remarque']:
        suivi.remarque = request.POST['remarque']
    else:
        suivi.remarque = None
    form = SuiviForm(data=request.POST)

    if form.is_valid():
        print('form is valid')
        suivi.save()
        if request.POST.get('previous', None):
            return redirect(request.POST.get('previous', None))
        else:
            if etat == 'TOUS':
                etat = None
            return list_suivis(request,
                               datetime.strptime(request.POST['date_debut'], '%d/%m/%Y'),
                               datetime.strptime(request.POST['date_fin'], '%d/%m/%Y'), etat)
    else:
        print('form is invalid')
        return render(request, "suivi/suivi_form.html",
                      {'suivi':      suivi,
                       'form': form})

