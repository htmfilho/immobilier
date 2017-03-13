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
from main.models import *
from django.shortcuts import render, redirect
from datetime import datetime
from main.forms import FinancementLocationForm

from main import models as mdl

def new(request, location_id):
    location = mdl.contrat_location.find_by_id(location_id)

    # Trouver le dernier financement
    financement_list = mdl.financement_location.find_by_location(location_id).order_by('date_debut')

    nouveau_financement = None
    financement = None
    if financement_list:
        financement = financement_list[0]
        # le dupliquer
        nouveau_financement = mdl.financement_location.FinancementLocation()
        nouveau_financement.date_debut = financement.date_debut
        nouveau_financement.date_fin = financement.date_fin
        nouveau_financement.loyer = financement.loyer
        nouveau_financement.charges = financement.charges
        nouveau_financement.index = financement.index

    return render(request, "financementlocation_new.html",
                  {'old_financement': financement,
                   'nouveau_financement': nouveau_financement,
                   'id_location': location.id})


def create(request):
    if request.POST.get('cancel_financement_loc_new', None):
        previous = request.POST.get('previous', None)
        return redirect(previous)
    else:
        form = FinancementLocationForm(data=request.POST)
        prev = request.POST.get('prev', None)
        location = mdl.contrat_location.find_by_id(request.POST['id'])
        # todo : récupérer le nouveau financement, adapter l'ancien et sauver le tout en bd
        # adaptation du financement courant
        financement_courant = location.financement_courant
        date_fin_initiale = financement_courant.date_fin
        dd = None
        if request.POST['date_debut']:
            dd = datetime.strptime(request.POST['date_debut'], '%d/%m/%Y')

        financement_courant.date_fin = dd
        financement_courant.save()
        # creation du nouveau financement
        nouveau_financement = mdl.financement_location.FinancementLocation()
        nouveau_financement.date_debut = dd
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
        # on doit adapter les suivis existantes
        suivis_existant = mdl.suivi_loyer.find(financement_courant, nouveau_financement.date_debut, 'A_VERIFIER')
        for s in suivis_existant:
            s.financement_location = nouveau_financement
            s.remarque = 'Nouveau financement'
            s.save()
        if prev == 'fl':
            return render(request, "contratlocation_update.html",
                          {'location': location})

        return redirect('/contratlocations/')
