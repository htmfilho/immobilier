from main.models import SuiviLoyer

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import datetime
from main.forms import SuiviForm
from django.shortcuts import redirect


def suivis_search(request):
    date_debut = request.GET['date_debut']
    date_fin = request.GET['date_fin']
    etat = request.GET['etat']

    if date_debut:
        date_debut = datetime.strptime(request.GET['date_debut'], '%d/%m/%Y')
    if date_fin:
        date_fin = datetime.strptime(request.GET['date_fin'], '%d/%m/%Y')
    if etat == 'TOUS':
        etat = None
    return list_suivis(request,date_debut,date_fin, etat)


def list_suivis(request, date_debut, date_fin, etat):
    suivis = SuiviLoyer.find_suivis(date_debut, date_fin, etat)
    if etat is None:
        etat = 'TOUS'
    return render(request, "suivis.html",
                  {'date_debut': date_debut,
                   'date_fin':    date_fin,
                   'etat':        etat,
                   'suivis':      suivis})


def suivis(request):
    return render(request, "suivis.html",
                  {'date_debut':       timezone.now(),
                   'date_fin':         timezone.now() + relativedelta(months=1),
                   'suivis':           SuiviLoyer.find_all()
                  })


def refresh_suivis(request):
    print('refresh_suivis')
    date_debut = request.POST['date_debut']
    date_fin = request.POST['date_fin']
    etat =  request.POST['etat']
    if etat == "TOUS":
        etat = None
    # print(date_debut.strftime('%Y-%m-%d'))
    suivis = SuiviLoyer.find_suivis(date_debut,date_fin, etat)

    return render(request, "suivis.html",
                  {'date_debut':       date_debut,
                   'date_fin':         date_fin,
                   'suivis':           suivis
                  })

def suivis_update(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        for key, value in request.POST.iteritems():
            print (key, value)
            if key.startswith('suivi_'):
                print ('info suivis')


        pass

    date_debut = request.POST['date_debut']
    date_fin = request.POST['date_fin']
    etat =  request.POST['etat']
    if etat == "TOUS":
        etat = None
    # print(date_debut.strftime('%Y-%m-%d'))
    suivis = SuiviLoyer.find_suivis(date_debut,date_fin, etat)

    return render(request, "suivis.html",
                  {'date_debut':       date_debut,
                   'date_fin':         date_fin,
                   'suivis':           suivis
                  })

def suivis_updatel(request, suivi_id):
    print('suivis_updatel')
    suivi = get_object_or_404(SuiviLoyer, pk=suivi_id)
    # etat =  request.POST['etat']
    # print (etat)
    etat = request.GET['etat']
    date_debut = request.GET['dated']
    date_fin = request.GET['datef']
    if date_debut:
        date_debut = datetime.strptime(date_debut, '%d/%m/%Y')
    if date_fin:
        date_fin = datetime.strptime(date_fin, '%d/%m/%Y')

    # etat = request.GET['etat']
    return render(request, "suivi_form.html",
                  {'suivi':      suivi,
                   'date_debut': date_debut,
                   'date_fin':   date_fin,
                   'etat':       etat})

def update_suivi(request):
    etat = request.POST['etat']
    suivi = get_object_or_404(SuiviLoyer, pk=request.POST['id'])

    if request.POST['date_paiement_reel']:
        suivi.date_paiement_reel = datetime.strptime(request.POST['date_paiement_reel'], '%d/%m/%Y')
    else:
        suivi.date_paiement_reel = None

    if request.POST['etat_suivi']:
        suivi.etat_suivi=request.POST['etat_suivi']
    else:
        suivi.etat_suivi='A_VERIFIER'

    if request.POST['loyer_percu']:
        suivi.loyer_percu=request.POST['loyer_percu']
    else:
        suivi.loyer_percu=0

    if request.POST.get('charges_percu',None):
        suivi.charges_percu=request.POST['charges_percu']
    else:
        suivi.charges_percu=0

    if request.POST['remarque']:
        suivi.remarque = request.POST['remarque']
    else:
        suivi.remarque = None
    form = SuiviForm(data=request.POST)

    if form.is_valid():
        suivi.save()
        if request.POST.get('previous', None):
            return redirect(request.POST.get('previous',None))
        else:
            if etat == 'TOUS':
                etat = None
            return list_suivis(request, datetime.strptime(request.POST['date_debut'], '%d/%m/%Y'),datetime.strptime(request.POST['date_fin'], '%d/%m/%Y'), etat)
    else:
        return render(request, "suivi_form.html",
              {'suivi':      suivi,
               'form': form})

