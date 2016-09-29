from main.models import SuiviLoyer, ContratLocation, FinancementLocation
from django.shortcuts import render, redirect
from datetime import datetime
from main.forms import FinancementLocationForm


def new(request, location_id):
    location = ContratLocation.objects.get(pk=location_id)

    # Trouver le dernier financement
    financement_list = FinancementLocation.objects.filter(contrat_location=location.id).order_by('date_debut')

    nouveau_financement = None
    financement = None
    if financement_list:
        financement = financement_list[0]
        #le dupliquer
        nouveau_financement = FinancementLocation()
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
        location = ContratLocation.objects.get(pk=request.POST['id'])
        # todo : récupérer le nouveau financement, adapter l'ancien et sauver le tout en bd
        # adaptation du financement courant
        financement_courant = location.financement_courant
        date_fin_initiale = financement_courant.date_fin
        dd = None
        if request.POST['date_debut']:
            dd = datetime.strptime(request.POST['date_debut'], '%d/%m/%Y')

        financement_courant.date_fin = dd
        financement_courant.save
        # creation du nouveau financement
        nouveau_financement = FinancementLocation()
        nouveau_financement.date_debut = dd
        nouveau_financement.date_fin = date_fin_initiale  # j'estime que la date de fin ne change pas
        nouveau_financement.loyer = 0
        if request.POST.get('loyer',None):
            nouveau_financement.loyer = float(request.POST['loyer'].replace(',', '.'))

        nouveau_financement.charges = 0
        if request.POST.get('charges',None):
            nouveau_financement.charges = float(request.POST['charges'].replace(',', '.'))

        nouveau_financement.index = 0
        if request.POST.get('index',None):
            nouveau_financement.index = float(request.POST['index'].replace(',', '.'))


        nouveau_financement.contrat_location = location
        nouveau_financement.save()
        #on doit adapter les suivis existantes
        suivis_existant = SuiviLoyer.objects.filter(financement_location=financement_courant,
                                                    date_paiement__gte=nouveau_financement.date_debut,
                                                    etat_suivi='A_VERIFIER')
        for s in suivis_existant:
            s.financement_location = nouveau_financement
            s.remarque = 'Nouveau financement'
            s.save()
        if prev == 'fl':
            return render(request, "contratlocation_update.html",
                          {'location': location})

        return redirect('/contratlocations/')
