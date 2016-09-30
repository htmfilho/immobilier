from main.models import *
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from main.forms import FraisMaintenanceForm


def new(request):
    frais = FraisMaintenance()

    return render(request, "fraismaintenance_form.html",
                  {'frais':     frais,
                   'personnes': Personne.find_all(),
                   'action':   'new',
                   'batiments': Batiment.find_all(),
                   'entrepreneurs': Professionnel.find_all()})


def create(request, batiment_id):
    batiment = get_object_or_404(Batiment, pk=batiment_id)
    frais = FraisMaintenance()
    frais.batiment = batiment

    return render(request, "fraismaintenance_form.html",
                  {'frais':     frais,
                   'personnes': Personne.find_all(),
                   'action':   'new',
                   'entrepreneurs': Professionnel.find_all()})


def prepare_update(request, id):
    frais = FraisMaintenance.objects.get(pk=id)
    return render(request, "fraismaintenance_form.html",
                  {'frais':  frais,
                   'action': 'update',
                   'entrepreneurs': Professionnel.find_all()})


def update(request):
    if request.POST.get('action', None) == 'new':
        frais = FraisMaintenance()
        batiment = get_object_or_404(Batiment, pk=request.POST.get('batiment_id', None))
        frais.batiment = batiment
    else:
        frais = get_object_or_404(FraisMaintenance, pk=request.POST.get('id', None))

    professionnel = None
    if request.POST.get('entrepreneur', None) and request.POST['entrepreneur']!= '' and request.POST['entrepreneur']!='None':
        professionnel = get_object_or_404(Professionnel, pk=request.POST['entrepreneur'])

    frais.entrepreneur = professionnel
    if request.POST.get('societe', None):
        frais.societe = request.POST['societe']
    else:
        frais.societe = None
    if request.POST.get('description', None):
        frais.description = request.POST['description']
    else:
        frais.description = None

    if request.POST.get('montant', None):
        frais.montant = float(request.POST['montant'].replace(',', '.'))
    else:
        frais.montant = 0
    if request.POST.get('date_realisation', None):
        valid_datetime = datetime.strptime(request.POST['date_realisation'], '%d/%m/%Y')
        frais.date_realisation = valid_datetime
    else:
        frais.date_realisation = None
    form = FraisMaintenanceForm(data=request.POST)
    if form.is_valid():
        frais.save()
        previous = request.POST.get('previous', None)
        return redirect(previous)
    else:
        return render(request, "fraismaintenance_form.html", {
             'frais': frais,
             'form': form,
             'action': 'update',
             'entrepreneurs': Professionnel.find_all()})


def list(request):
    frais_list = FraisMaintenance.objects.all()
    return render(request, "fraismaintenance_list.html",
                           {'frais_list': frais_list})


def delete(request, id):
    frais = get_object_or_404(FraisMaintenance, pk=id)
    batiment = frais.batiment
    if frais:
        frais.delete()
    return render(request, "fraismaintenance_confirm_delete.html",
                           {'object': frais})
