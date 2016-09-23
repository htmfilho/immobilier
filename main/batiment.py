from main.models import *
from django.shortcuts import render, get_object_or_404


def create(request):
    batiment = Batiment()
    return render(request, "batiment_form.html",
                  {'batiment':         batiment,
                   'localites':    Localite.find_all()})


def batiment_form(request, batiment_id):
    print('batiment_form')
    batiment = Batiment.find_batiment(batiment_id)

    return render(request, "batiment_form.html",
                  {'batiment':     batiment,
                   'assurances':   Assurance.find_all(),
                   'localites':    Localite.find_all()})


def update(request):

    batiment = Batiment()

    if 'add' == request.POST['action'] or 'modify' == request.POST['action']:
        if request.POST['id'] and not request.POST['id'] == 'None':
            batiment = get_object_or_404(Batiment, pk=request.POST['id'])
        else:
            batiment = Batiment()
        batiment.rue = request.POST['rue']
        print(request.POST['numero'])
        batiment.numero = request.POST['numero']
        batiment.boite = request.POST['boite']
        localite = None
        if request.POST['localite']:
            localite = get_object_or_404(Localite, pk=request.POST['localite'])

        batiment.localite = localite

        if request.POST['superficie']:
            batiment.superficie = float(request.POST['superficie'].strip().replace(',', '.'))
        else:
            batiment.superficie = None

        if request.POST['performance_energetique']:
            batiment.performance_energetique = float(request.POST['performance_energetique'].strip().replace(',', '.'))
        else:
            batiment.performance_energetique = None

        batiment.save()

    return render(request, "batiment_form.html",
                  {'batiment':     batiment,
                   'localites':    Localite.find_all()})
