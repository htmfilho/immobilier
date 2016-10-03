from main.models import Societe, Personne
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from main.forms import PersonneForm


def edit(request, personne_id):
    if personne_id:
        personne = Personne.find_personne(personne_id)
    else:
        personne = Personne()
    return render(request, "personne_form.html",
                  {'personne': personne,
                   'societes': Societe.find_all()})


def create(request):
    return render(request, "personne_form.html",
                  {'personne': Personne(),
                   'societes': Societe.find_all()})


def list(request):
    return render(request, "personne_list.html",
                  {'personnes': Personne.find_all()})


def search(request):
    nom = request.GET.get('nom')
    prenom = request.GET.get('prenom')

    query = Personne.find_all()

    if nom:
        query = query.filter(nom__icontains=nom)
    if prenom:
        query = query.filter(prenom__icontains=prenom)

    return render(request, "personne_list.html",
                  {'nom': nom,
                   'prenom': prenom,
                   'personnes': query})


def update(request):
    form = PersonneForm(data=request.POST)
    if request.POST['personne_id'] and not request.POST['personne_id'] == 'None':
        personne = get_object_or_404(Personne, pk=request.POST['personne_id'])
    else:
        personne = Personne()

    personne.nom =request.POST['nom']
    personne.prenom =request.POST['prenom']
    personne.email =request.POST['email']
    personne.profession =request.POST['profession']
    personne.societe = None
    if request.POST.get('societe', None):
        if request.POST['societe']!='':
            societe = Societe.find_by_id(int(request.POST['societe']))
            personne.societe=societe

    personne.lieu_naissance = request.POST['lieu_naissance']
    personne.pays_naissance = request.POST['pays_naissance']
    personne.num_identite = request.POST['num_identite']
    personne.num_compte_banque = request.POST['num_compte_banque']

    personne.telephone =request.POST['telephone']
    personne.gsm = request.POST['gsm']
    if request.POST['date_naissance']:
        try:
            personne.date_naissance = datetime.strptime(request.POST['date_naissance'], '%d/%m/%Y')
        except ValueError:
            personne.date_naissance = request.POST['date_naissance']
    else:
        personne.date_naissance = None
    if form.is_valid():
        personne.save()
        return render(request, "personne_list.html",
                      {'personnes': Personne.find_all()})
    else:
        return render(request, "personne_form.html",
                      {'personne': personne,
                       'form': form,
                       'societes': Societe.find_all()})
