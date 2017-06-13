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
from django.shortcuts import render
from main import models as mdl
from main.models.enums import alerte_etat


def list(request):
    return render(request, "alerte/alerte_list.html",
                  {'alertes': mdl.alerte.find_by_etat(alerte_etat.VERIFIER)})


def update_a_verifier(request):
    etat_alerte = request.POST.get('txt_etat_alerte')
    save_alerte(request.POST.get('alerte_id'))

    return render_alerte(etat_alerte, request)


def search(request):
    return render_alerte(request.GET.get('etat_alerte'), request)


def render_alerte(etat_alerte, request):
    if etat_alerte:
        return render(request, "alerte/alerte_list.html",
                      {'alertes': mdl.alerte.find_by_etat(etat_alerte),
                       'etat_alerte': etat_alerte})
    else:
        return render(request, "alerte/alerte_list.html",
                      {'alertes': mdl.alerte.find_all()})


def save_alerte(alerte_id):
    if alerte_id:
        alerte = mdl.alerte.find_by_id(alerte_id)
        alerte.etat = alerte_etat.VERIFIER
        alerte.save()
