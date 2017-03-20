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
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from main import models as mdl


def societe_liste(request):
    print('societe_liste')
    return render(request, 'liste_societes.html', {'societes': mdl.societe.find_all()})


def update(request):
    societe_id = None
    if request.POST['societe_id']:
        societe_id = int(request.POST['societe_id'])
    print(societe_id)
    if societe_id:
        societe = get_object_or_404(mdl.societe.Societe, pk=societe_id)
    else:
        societe = mdl.societe.Societe()

    societe.nom = request.POST['nom']
    societe.description = request.POST['description']
    societe.rue = request.POST['rue']
    if request.POST['numero'] != '':
        societe.numero = request.POST['numero']
    else:
        societe.numero = None
    societe.boite = request.POST['boite']
    societe.lieu_dit =request.POST['lieu_dit']
    societe.localite = None
    print(request.POST['localite'])
    if request.POST['localite']:
        if request.POST['localite'] != '':
            societe.localite = mdl.localite.find_by_id(int(request.POST['localite']))

    societe.save()
    return HttpResponseRedirect(reverse('home'))


def edit(request, societe_id):
    if societe_id:
        societe = get_object_or_404(mdl.societe.Societe, pk=societe_id)
    else:
        societe = mdl.societe.Societe()
    return render(request, "societe_form.html",
                  {'societe': societe,
                   'localites': mdl.localite.find_all()})
