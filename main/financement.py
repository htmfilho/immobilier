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
from django.shortcuts import render, redirect
from datetime import datetime
from main import models as mdl
from dateutil.relativedelta import relativedelta


def new(request, location_id):
    location = mdl.contrat_location.find_by_id(location_id)

    # Trouver le dernier financement
    financement_list = mdl.financement_location.find_by_location(location_id).order_by('date_debut')
    financement_dernier = financement_list.last()

    nouveau_financement = None
    financement = None
    if financement_list:
        financement = financement_list[0]
        # le dupliquer
        nouveau_financement = mdl.financement_location.FinancementLocation()
        nouveau_financement.date_debut = financement_dernier.date_debut
        nouveau_financement.date_fin = financement_dernier.date_fin
        nouveau_financement.loyer = financement_dernier.loyer
        nouveau_financement.charges = financement_dernier.charges
        nouveau_financement.index = financement_dernier.index

    return render(request, "financementlocation_new.html",
                  {'old_financement': financement,
                   'nouveau_financement': nouveau_financement,
                   'id_location': location.id,
                   'prev': request.GET.get('prev', None) })


def create(request):
    if request.POST.get('cancel_financement_loc_new', None):
        previous = request.POST.get('previous', None)
        return redirect(previous)
    else:
        prev = request.POST.get('prev', None)
        location = mdl.contrat_location.find_by_id(request.POST['id'])
        # todo : récupérer le nouveau financement, adapter l'ancien et sauver le tout en bd
        # adaptation du financement courant
        financement_courant = location.dernier_financement

        financement_list = mdl.financement_location.find_by_location(location.id).order_by('date_debut')
        financement_dernier = financement_list.last()
        date_fin_initiale = location.date_fin

        nouvelle_date_fin_financement_courant = modifer_date_fin_financement_courant(financement_courant, request)

        nouveau_financement = nouveau_financement_depuis_precedant(date_fin_initiale, location,
                                                                   nouvelle_date_fin_financement_courant, request)

        # on doit adapter les suivis existantes
        suivis_existant = mdl.suivi_loyer.find(financement_courant, nouveau_financement.date_debut, 'A_VERIFIER')
        for s in suivis_existant:
            s.financement_location = nouveau_financement
            s.remarque = 'Indexé'
            s.save()

        financement_courant = mdl.financement_location.find_by_id(location.financement_courant.id)

        if prev == 'fl':
            return render(request, "contratlocation_update.html",
                          {'location': location})

        return redirect('/contratlocations/')


def nouveau_financement_depuis_precedant(date_fin_initiale, location, nouvelle_date_fin_financement_courant, request):
    # creation du nouveau financement
    nouveau_financement = mdl.financement_location.FinancementLocation()
    nouveau_financement.date_debut = nouvelle_date_fin_financement_courant + relativedelta(days=1)
    nouveau_financement.date_fin = date_fin_initiale  # j'estime que la date de fin ne change pas
    nouveau_financement.loyer = 0
    if request.POST.get('loyer', None):
        nouveau_financement.loyer = float(request.POST['loyer'].replace(',', '.'))
    nouveau_financement.charges = 0
    if request.POST.get('charges', None):
        nouveau_financement.charges = float(request.POST['charges'].replace(',', '.'))
    nouveau_financement.index = 0
    if request.POST.get('index', None):
        nouveau_financement.index = float(request.POST['index'].replace(',', '.'))
    nouveau_financement.contrat_location = location
    nouveau_financement.save()
    return nouveau_financement


def modifer_date_fin_financement_courant(financement_courant, request,):
    nouvelle_date_de_fin = None
    if request.POST['date_debut']:
        nouvelle_date_de_fin = datetime.strptime(request.POST['date_debut'], '%d/%m/%Y')
        nouvelle_date_de_fin = nouvelle_date_de_fin - relativedelta(days=1)

    financement_courant.date_fin = nouvelle_date_de_fin
    financement_courant.save()

    return nouvelle_date_de_fin
