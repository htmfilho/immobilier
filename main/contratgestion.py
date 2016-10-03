from main.models import *
from django.shortcuts import render, get_object_or_404, redirect
from main.forms import ContratGestionForm
from datetime import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext


def new(request):
    contrat = ContratGestion()
    personne_gestionnaire = Personne.find_gestionnaire_default()
    if personne_gestionnaire:
        contrat.gestionnaire = personne_gestionnaire
    batiments = Batiment.objects.all()
    return render(request, "contratgestion_update.html",
                  {'contrat':   contrat,
                   'personnes': Personne.find_all(),
                   'action':   'new',
                   'prev':      'fb',
                   'batiments': batiments})


def create(request, batiment_id):
    """
    ok - 1
    """
    batiment = get_object_or_404(Batiment, pk=batiment_id)
    contrat = ContratGestion()
    contrat.batiment = batiment
    # Par défaut Sté comme gestionnaire

    personne_gestionnaire = Personne.find_gestionnaire_default()
    if personne_gestionnaire:
        contrat.gestionnaire = personne_gestionnaire
    return render(request, "contratgestion_update.html",
                  {'contrat':   contrat,
                   'personnes': Personne.find_all(),
                   'action':   'new',
                   'prev':      'fb'})


def prepare_update(request, id):
    contrat = ContratGestion.objects.get(pk=id)
    personnes = []
    personne_gestionnaire = Personne.find_gestionnaire_default()
    personnes.append(personne_gestionnaire)
    return render(request, "contratgestion_update.html",
                  {'contrat':   contrat,
                   'action':   'update',
                   'personnes': personnes})


def update(request):
    """
    ok - 1
    """
    previous = request.POST.get('previous', None)
    form = ContratGestionForm(data=request.POST)
    gestion = None
    personne = None
    batiment_id = request.POST.get('batiment_id', None)
    if batiment_id == "":
        batiment_id = None
    if request.POST.get('action', None) == 'new':
        gestion = ContratGestion()
        batiment = get_object_or_404(Batiment, pk=batiment_id)
        gestion.batiment = batiment
    else:
        if request.POST.get('id', None) != '':
            gestion = get_object_or_404(ContratGestion, pk=request.POST.get('id', None))
            batiment = get_object_or_404(Batiment, pk=batiment_id)
            gestion.batiment = batiment
    if gestion is None:
        gestion = ContratGestion()
        batiment = get_object_or_404(Batiment, pk=batiment_id)
        gestion.batiment = batiment
    if request.POST.get('gestionnaire', None):
        personne = get_object_or_404(Personne, pk=request.POST.get('gestionnaire', None))
        gestion.gestionnaire = personne
    if request.POST.get('montant_mensuel', None):
        gestion.montant_mensuel = request.POST.get('montant_mensuel')
    if request.POST.get('date_debut', None):
        try:
            valid_datetime = datetime.strptime(request.POST['date_debut'], '%d/%m/%Y')
            gestion.date_debut = valid_datetime
        except:
            gestion.date_debut = None
    else:

        gestion.date_debut = None

    # gestion.date_fin = request.POST['date_fin']
    if request.POST.get('date_fin', None):
        try:
            valid_datetime = datetime.strptime(request.POST['date_fin'], '%d/%m/%Y')
            gestion.date_fin = valid_datetime
        except:
            gestion.date_fin = None
    else:
        gestion.date_fin = None
    if gestion.date_debut and gestion.date_fin:
        if gestion.date_debut > gestion.date_fin:
            return render(request, "contratgestion_update.html",
                          {'contrat': gestion,
                           'message': 'La date de début doit être < à la date de fin'})
    if personne is None:
        message = "Il faut sélectionner un gestionnaire"
        return render(request, "contratgestion_update.html",
                      {'contrat': gestion,
                       'action':   'update',
                       'message': message,
                       'form':     form})
    if form.is_valid() and data_valid(form, gestion):
        montant_mensuel = request.POST.get('montant_mensuel', None)
        if montant_mensuel:
            try:
                gestion.montant_mensuel = float(montant_mensuel.replace(',', '.'))
            except:
                gestion.montant_mensuel = None
        gestion.save()
        return redirect(previous)
    else:
        personnes = []
        personne_gestionnaire = Personne.find_gestionnaire_default()
        personnes.append(personne_gestionnaire)

        return render_to_response( "contratgestion_update.html",
                      {'contrat': gestion,
                       'action': 'update',
                       'message': 'Invalide',
                       'form': form,
                       'personnes': personnes,
                       'batiments': Batiment.objects.all()},context_instance=RequestContext(request))
        # return render_to_response('new_stmt.html', {'form': form, },context_instance=RequestContext(request))


def list(request):
    contrats = ContratGestion.objects.all()
    return render(request, "contratgestion_list.html",
                           {'contrats': contrats})


def delete(request, contrat_gestion_id):
    contrat_gestion = get_object_or_404(ContratGestion, pk=contrat_gestion_id)
    batiment = contrat_gestion.batiment
    if contrat_gestion:
        contrat_gestion.delete()
    return render(request, "batiment_form.html", {'batiment': batiment})


def data_valid(form, contrat):
    # contrat = ContratGestion.search(contrat.batiment, contrat.date_debut, contrat.date_fin)
    # if contrat.exists():
    #
    #     return False
    return True