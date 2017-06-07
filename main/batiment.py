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
from main.forms import BatimentForm
from main import models as mdl


def create(request):
    batiment = mdl.batiment.Batiment()
    return render(request, "batiment_form.html",
                  {'batiment':         batiment,
                   'localites':    mdl.localite.find_all()})


def batiment_form(request, batiment_id):
    batiment = mdl.batiment.find_batiment(batiment_id)

    return render(request, "batiment_form.html",
                  {'batiment':     batiment,
                   'assurances':   mdl.assurance.find_all(),
                   'localites':    mdl.localite.find_all()})


def update(request):
    batiment = mdl.batiment.Batiment()
    message_info = None
    form = None
    if 'add' == request.POST.get('action') or 'modify' == request.POST.get('action'):
        form = BatimentForm(data=request.POST)
        if request.POST.get('id') and not request.POST['id'] == 'None':
            batiment = get_object_or_404(mdl.batiment.Batiment, pk=request.POST['id'])
        else:
            batiment = mdl.batiment.Batiment()
        batiment.rue = request.POST['rue']
        if request.POST['numero'] and request.POST['numero'] != '':
            batiment.numero = request.POST['numero']
        else:
            batiment.numero = None
        if request.POST['numero'] and request.POST['boite'] != '':
            batiment.boite = request.POST['boite']
        else:
            batiment.boite = None
        localite = None
        if request.POST['localite_cp'] and request.POST['localite_cp'] != '' \
                and request.POST['localite_nom'] and request.POST['localite_nom'] != '':
            print(request.POST['localite_cp'])
            print(request.POST['localite_nom'])
            localites = mdl.localite.search(request.POST['localite_cp'], request.POST['localite_nom'])
            if not localites.exists():
                localite = mdl.localite.Localite()
                localite.localite = request.POST['localite_nom']
                localite.code_postal = request.POST['localite_cp']
                localite.save()
            else:
                localite = localites[0]

        batiment.localite = localite

        if request.POST['superficie']:
            batiment.superficie = request.POST['superficie']
        else:
            batiment.superficie = None

        if request.POST['performance_energetique'] and request.POST['performance_energetique'] != '':
            batiment.performance_energetique = request.POST['performance_energetique']
        else:
            batiment.performance_energetique = None
        if request.POST['description']:
            batiment.description = request.POST['description']
        else:
            batiment.description = None

        if form.is_valid():
            batiment.save()
            message_info = "Données sauvegardées"

    return render(request, "batiment_form.html",
                  {'batiment':     batiment,
                   'localites':    mdl.localite.find_all(),
                   'message_info': message_info,
                   'form': form})


def search(request):
    proprietaire = request.GET.get('proprietaire', None)
    batiments = mdl.batiment.search(proprietaire)
    return render(request, 'batiment/listeBatiments.html',
                  {'batiments': batiments,
                   'proprietaires': mdl.proprietaire.find_distinct_proprietaires()})


def delete(request, batiment_id):
    print('delete', batiment_id)
    if batiment_id:
        batiment = get_object_or_404(mdl.batiment.Batiment, pk=batiment_id)
        if batiment:
            batiment.delete()

    return search(request)

