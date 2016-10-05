from main.models import *
from django.shortcuts import render, get_object_or_404


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

    if 'add' == request.POST.get('action') or 'modify' == request.POST.get('action'):
        if request.POST.get('id') and not request.POST['id'] == 'None':
            batiment = get_object_or_404(Batiment, pk=request.POST['id'])
        else:
            batiment = Batiment()
        batiment.rue = request.POST['rue']
        print(request.POST['numero'])
        batiment.numero = request.POST['numero']
        batiment.boite = request.POST['boite']

        localite = None
        if request.POST['localite_cp'] and request.POST['localite_cp'] != '' \
                and request.POST['localite_nom'] and request.POST['localite_nom'] != '':
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
            batiment.superficie = float(request.POST['superficie'].strip().replace(',', '.'))
        else:
            batiment.superficie = None

        if request.POST['performance_energetique']:
            batiment.performance_energetique = float(request.POST['performance_energetique'].strip().replace(',', '.'))
        else:
            batiment.performance_energetique = None
        if request.POST['description']:
            batiment.description = request.POST['description']
        else:
            batiment.description = None
        batiment.save()
    message_info = "Données sauvegardées"
    return render(request, "batiment_form.html",
                  {'batiment':     batiment,
                   'localites':    Localite.find_all(),
                   'message_info': message_info})


def search(request):
    proprietaire = request.GET.get('proprietaire', None)
    batiments = Batiment.search(proprietaire)
    return render(request, 'listeBatiments.html', {'batiments': batiments,
                                                   'proprietaires': Proprietaire.find_distinct_proprietaires()})
