##############################################################################
#
#    Immobilier it's an application
#    designed to manage the core business of property management, buildings,
#    rental agreement and so on.
#
#    Copyright (C) 2016-2018 Verpoorten Leïla
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
from django.shortcuts import redirect
from main import models as mdl
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from main.models.enums import etat_suivi
from decimal import Decimal
from main.views_utils import get_date, UNDEFINED
from main.forms import SuiviForm
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required


TOUS = 'TOUS'
SUIVI_SUIVIS_HTML = "suivi/suivis.html"


@login_required
@require_GET
def suivis_search(request):
    etat = request.GET['etat']
    date_debut = get_date(request.GET.get('date_debut', None))
    date_fin = get_date(request.GET.get('date_fin', None))
    if etat == TOUS:
        etat = None
    return list_suivis(request, date_debut, date_fin, etat)


def list_suivis(request, date_debut, date_fin, etat):
    return render(request, SUIVI_SUIVIS_HTML,
                  {'date_debut': date_debut,
                   'date_fin':    date_fin,
                   'etat':        etat,
                   'suivis':      mdl.suivi_loyer.find_suivis(date_debut, date_fin, etat)})


@login_required
def suivis(request):
    date_fin = timezone.now() - relativedelta(days=1)
    return render(request, "suivi/suivis.html",
                  {'date_debut':       None,
                   'etat': etat_suivi.A_VERIFIER,
                   'date_fin':         date_fin,
                   'suivis':           mdl.suivi_loyer.find_suivis(None, date_fin, None)
                   })


@login_required
def refresh_suivis(request):
    date_debut = request.POST['date_debut']
    date_fin = request.POST['date_fin']
    etat = get_post_etat(request)
    return render(request, "suivi/suivis.html",
                  {'date_debut':       date_debut,
                   'date_fin':         date_fin,
                   'suivis':           mdl.suivi_loyer.find_suivis(date_debut, date_fin, etat)
                   })


@login_required
def suivis_update(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        for key, value in request.POST.iteritems():
            if key.startswith('suivi_'):
                print('info suivis')

        pass

    date_debut = request.POST['date_debut']
    date_fin = request.POST['date_fin']
    etat = get_post_etat(request)
    return render(request, "suivi/suivis.html",
                  {'date_debut':       date_debut,
                   'date_fin':         date_fin,
                   'suivis':           mdl.suivi_loyer.find_suivis(date_debut, date_fin, etat)
                   })


@login_required
@require_GET
def suivis_updatel(request, suivi_id, previous):
    suivi = get_object_or_404(mdl.suivi_loyer.SuiviLoyer, pk=suivi_id)
    etat = request.GET.get('etat', None)
    form = SuiviForm(instance=suivi)

    date_debut = get_date(request.GET.get('dated', None))
    date_fin = get_date(request.GET.get('datef', None))

    return render(request, "suivi/suivi_form.html",
                  {'suivi':      suivi,
                   'date_debut': date_debut,
                   'date_fin':   date_fin,
                   'etat':       etat,
                   'previous': previous,
                   'form': form})


@login_required
@require_POST
def update_suivi(request):
    suivi = get_object_or_404(mdl.suivi_loyer.SuiviLoyer, pk=request.POST.get('id', None))
    etat = get_post_etat(request)
    date_debut = get_date(request.POST.get('date_debut', None))
    date_fin = get_date(request.POST.get('date_fin', None))
    previous = request.POST.get('previous', None)
    form = SuiviForm(request.POST, instance=suivi)
    if request.method == 'POST':
        if form.is_valid():
            suivi = form.save()
        else:
            suivi = mdl.suivi_loyer.find_by_id(request.POST)
            return render(request, "suivi/suivi_form.html",
                          {'suivi':      suivi,
                           'previous': previous,
                           'etat': etat,
                           'form': form})

    if previous:
        return redirection_suivi(previous, request, suivi, etat, date_debut, date_fin)
    else:
        return list_suivis(request,
                           get_date(request.POST.get('date_debut', None)),
                           get_date(request.POST.get('date_fin', None)),
                           etat)


def redirection_suivi(previous, request, suivi, etat, date_debut, date_fin):
    if previous == 'liste':
        # date_fin = timezone.now() - relativedelta(days=1)
        return render(request, "suivi/suivis.html",
                      {'date_debut': date_debut,
                       'etat': etat,
                       'date_fin': date_fin,
                       'suivis': mdl.suivi_loyer.find_suivis(date_debut, date_fin, etat)
                       })
    if previous == 'home':
        return redirect("home")
    if previous == 'location':
        return HttpResponseRedirect(reverse('location-prepare-update-all',
                                            args=(suivi.financement_location.contrat_location.id,)))
    return redirect(request.POST.get('previous', None))


def get_post_etat(request):
    etat = request.POST.get('etat', None)
    if etat == TOUS:
        return None
    return etat


def get_montant(valeur):
    try:
        return Decimal(valeur)
    except:
        return 0


def get_etat_suivi(request):
    etat_suivi = request.POST.get('etat_suivi', None)
    if etat_suivi:
        if etat_suivi == UNDEFINED or etat_suivi == TOUS:
            return None
        else:
            return etat_suivi
    else:
        return 'A_VERIFIER'


def suivis_update_liste(request, suivi_id):
    return suivis_updatel(request, suivi_id, 'liste')


def suivis_update_home(request, suivi_id):
    return suivis_updatel(request, suivi_id, 'home')


def suivis_update_location(request, suivi_id):
    return suivis_updatel(request, suivi_id, 'location')
