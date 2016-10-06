from main.models import *
from django.shortcuts import render, get_object_or_404
from main.forms import BatimentForm


def create(request):
    batiment = Batiment()
    return render(request, "batiment_form.html",
                  {'batiment':         batiment,
                   'localites':    Localite.find_all()})


def batiment_form(request, batiment_id):
    batiment = Batiment.find_batiment(batiment_id)

    return render(request, "batiment_form.html",
                  {'batiment':     batiment,
                   'assurances':   Assurance.find_all(),
                   'localites':    Localite.find_all()})


def update(request):

    batiment = Batiment()
    message_info = None
    if 'add' == request.POST.get('action') or 'modify' == request.POST.get('action'):
        form = BatimentForm(data=request.POST)
        if request.POST.get('id') and not request.POST['id'] == 'None':
            batiment = get_object_or_404(Batiment, pk=request.POST['id'])
        else:
            batiment = Batiment()
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
            localites = Localite.search(request.POST['localite_cp'], request.POST['localite_nom'])
            if not localites.exists():
                localite = Localite()
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
                   'localites':    Localite.find_all(),
                   'message_info': message_info,
                   'form':form})


def search(request):
    proprietaire = request.GET.get('proprietaire', None)
    batiments = Batiment.search(proprietaire)
    return render(request, 'listeBatiments.html', {'batiments': batiments,
                                                   'proprietaires': Proprietaire.find_distinct_proprietaires()})

def delete(request, batiment_id):
    print('delete',batiment_id)
    if batiment_id:
        batiment = get_object_or_404(Batiment, pk=batiment_id)
        if batiment:
            batiment.delete()

    return search(request)
