from main.models import *
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime


def new(request):
    frais = FraisMaintenance()

    return render(request, "fraismaintenance_form.html",
                  {'frais':     frais,
                   'personnes': Personne.find_all(),
                   'action':   'new',
                   'batiments': Batiment.find_all()})


def create(request, batiment_id):
    batiment = get_object_or_404(Batiment, pk=batiment_id)
    frais = FraisMaintenance()
    frais.batiment = batiment

    return render(request, "fraismaintenance_form.html",
                  {'frais':     frais,
                   'personnes': Personne.find_all(),
                   'action':   'new'})


def prepare_update(request, id):
    frais = FraisMaintenance.objects.get(pk=id)
    return render(request, "fraismaintenance_form.html",
                  {'frais':  frais,
                   'action': 'update'})


def update(request):
    if request.POST.get('action', None) == 'new':
        frais = FraisMaintenance()
        batiment = get_object_or_404(Batiment, pk=request.POST.get('batiment_id', None))
        frais.batiment = batiment
    else:
        frais = get_object_or_404(FraisMaintenance, pk=request.POST.get('id', None))
        batiment = frais.batiment

    if request.POST.get('entrepreneur', None):
        frais.entrepreneur = request.POST['entrepreneur']
    else:
        frais.entrepreneur = None
    if request.POST.get('societe', None):
        frais.societe = request.POST['societe']
    else:
        frais.societe = None
    if request.POST.get('description', None):
        frais.description = request.POST['description']
    else:
        frais.description = None

    if request.POST.get('montant', None):
        frais.montant = request.POST['montant']
    else:
        frais.montant = 0
    if request.POST.get('date_realisation', None):
        valid_datetime = datetime.strptime(request.POST['date_realisation'], '%d/%m/%Y')
        frais.date_realisation = valid_datetime
    else:
        frais.date_realisation = None

    frais.save()

    previous = request.POST.get('previous', None)
    return redirect(previous)


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
