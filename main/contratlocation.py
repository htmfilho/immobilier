from main.models import*
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from datetime import date
from datetime import datetime
from main.forms import ContratLocationForm
from dateutil.relativedelta import relativedelta


def prepare_update(request, location_id):
    location = ContratLocation.objects.get(pk=location_id)
    return render(request, "contratlocation_update.html",
                  {'location':    location,
                   'assurances': Assurance.find_all(), })


def update(request):
    previous = request.POST.get('previous', None)
    id = request.POST.get('id', None)
    form = ContratLocationForm(data=request.POST)
    location = get_object_or_404(ContratLocation, pk=id)
    prolongation_action = False
    if 'bt_prolongation' in request.POST:
        prolongation_action = True

    if request.POST['renonciation']:
        location.renonciation = datetime.strptime(request.POST['renonciation'], '%d/%m/%Y')
    location.remarque = request.POST['remarque']

    if request.POST['assurance'] and not request.POST['assurance'] == '-':
        location.assurance = get_object_or_404(Assurance, pk=request.POST['assurance'])
    else:
        location.assurance = None

    if form.is_valid():
        if prolongation_action and (request.POST.get('type_prolongation') == '1' \
                                    or request.POST.get('type_prolongation') == '7'):
            # Les financements seront adaptés via le save
            location.save_prolongation(int(request.POST.get('type_prolongation')))
        else:
            location.save_new()

        return redirect(previous)

    else:
        return render(request, "contratlocation_update.html",
                               {'location':    location,
                                'assurances':  Assurance.find_all(),
                                'nav':         'list_batiment',
                                'form':        form,
                                'previous':    previous})


def contrat_location_for_batiment(request, batiment_id):
    batiment = get_object_or_404(Batiment, pk=batiment_id)
    if batiment.location_actuelle:
        location = get_object_or_404(ContratLocation, pk=batiment.location_actuelle.id)
    else:
        location = None
    nouvelle_location = ContratLocation()
    if batiment:
        nouvelle_location.batiment = batiment
    if location is not None:
        nouvelle_location.date_debut = location.date_fin
        nouvelle_location.date_fin = location.date_fin + relativedelta(years=1)
        nouvelle_location.loyer_base = location.loyer_base
        nouvelle_location.charges_base = location.charges_base
    else:
        auj = date.today()
        nouvelle_location.date_debut = auj.strftime("%d/%m/%Y")

        # le financement sera crée automatiquement
    return render(request, "contratlocation_new.html",
                           {'location': nouvelle_location,
                            'assurances': Assurance.find_all(),
                            'nav': 'list_batiment'})


def list(request):
    date_fin = timezone.now()
    locations = ContratLocation.search(date_fin)
    return render(request, "contratlocation_list.html",
                           {'locations': locations,
                            'date_fin_filtre_location': date_fin})


def delete(request, location_id):
    location = get_object_or_404(ContratLocation, pk=location_id)
    if location:
        location.delete()
    return render(request, "contratlocation_confirm_delete.html",
                           {'object': location})


def confirm_delete(request):
    return redirect('/contratlocations/')


def test(request):
    """
    ok - 1
    """
    form = ContratLocationForm(data=request.POST)

    batiment = get_object_or_404(Batiment, pk=request.POST['batiment_id'])
    location = ContratLocation()
    location.batiment = batiment
    if request.POST['date_debut']:
        location.date_debut = datetime.strptime(request.POST['date_debut'], '%d/%m/%Y')
        location.date_fin = location.date_debut + relativedelta(years=1)
        location.renonciation = location.date_debut + relativedelta(days=355)
    else:
        location.date_debut = None
    # if request.POST.get('date_fin'):
    #     location.date_fin = datetime.strptime(request.POST['date_fin'], '%d/%m/%Y')
    # else:
    #     location.date_fin = None

    # if request.POST.get('renonciation'):
    #     location.renonciation = request.POST['renonciation']
    # else:
    #     location.renonciation = None
    location.remarque = request.POST['remarque']
    if request.POST.get('nom_assurance_other'):
        assurance = Assurance()
        assurance.nom = request.POST.get('nom_assurance_other')
        assurance.save()
        location.assurance = assurance
    else:
        if request.POST['assurance'] and not request.POST['assurance'] == 'None':
            location.assurance = get_object_or_404(Assurance, pk=request.POST['assurance'])
        else:
            location.assurance = None

    location.loyer_base = request.POST['loyer_base']
    location.charges_base = request.POST['charges_base']

    if form.is_valid():
        location.save_new()
        return HttpResponseRedirect(reverse('batiment', args=(location.batiment.id, )))
    else:
        return render(request, "contratlocation_new.html",
                               {'location':    location,
                                'assurances': Assurance.find_all(),
                                'nav':       'list_batiment',
                                'form': form})

    # if request.POST.get('prev', None) == 'fb':
    #     return render(request, "batiment_form.html",
    #                   {'batiment': batiment})
    #
    # lnk = None
    # if request.POST.get('return_lnk'):
    #     lnk = request.POST.get('return_lnk')
    #
    # if lnk:
    #     return redirect(lnk)
    # else:
    #     return redirect('/listeBatiments/')


def prolongation(request):
    id_location = request.GET['id_location']
    type_prolongation = request.GET['type_prolongation']
    location = get_object_or_404(ContratLocation, pk=id_location)
    # response = []
    if location:
        date_trav = location.date_fin
        if date_trav:
            if type_prolongation == "1":
                location.date_fin = date_trav + relativedelta(years=1)
                location.save()
                # response.append('date_fin',location.date_fin)
    # return HttpResponseRedirect(reverse('location-prepare-update-all', args=(id_location,)))
    # return HttpResponse('')
    # return redirect(reverse('location-prepare-update-all', args=(id_location,)))

    # return HttpResponse(simplejson.dumps(response))
    return render(request, "contratlocation_update.html",
                  {'location':    location,
                   'assurances': Assurance.find_all(), })


def contrat_location_form(request):
    nouvelle_location = ContratLocation()
    auj = date.today()
    nouvelle_location.date_debut = auj.strftime("%d/%m/%Y")
    return render(request, "contratlocation_form.html", {
                            'assurances': Assurance.find_all(),
                            'batiments': Batiment.find_all(),
                            'location': nouvelle_location,
                            'form': None})


def search(request):
    date_fin = request.GET.get('date_fin_filtre_location', None)
    if date_fin:
        date_fin = datetime.strptime(date_fin, '%d/%m/%Y')
        locations = ContratLocation.search(date_fin)
    else:
        locations = ContratLocation.find_all()
    return render(request, "contratlocation_list.html",
                           {'locations': locations,
                            'date_fin_filtre_location': date_fin})
