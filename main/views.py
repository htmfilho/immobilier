from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main.models import *
from django.views.generic import DetailView
from django.core.urlresolvers import reverse
import os
from .exportUtils import export_xls_batiment
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import datetime
from django.db import models
from django.views.generic import *
from django.core.urlresolvers import reverse_lazy
from main.forms import PersonneForm, BatimentForm, ProprietaireForm, FraisMaintenanceForm, SocieteForm, ContratLocationForm
import datetime

from dateutil.relativedelta import relativedelta
from . import batiment, proprietaire, suivis, alertes, contratlocation, financement, locataire, contratgestion


class ContratGestionList(ListView):
    model = ContratGestion

class ContratGestionDetail(DetailView):
    model = ContratGestion

class FraisMaintenanceList(ListView):
    model = FraisMaintenance

class FraisMaintenanceDetail(DetailView):
    model= FraisMaintenance


# Create your views here.
def dashboard(request):
    return render(request, 'main/dashboard.html', {})

def home(request):
    # return alertes.list(request)
    # return render(request, "home.html")
    date_debut = timezone.now(),
    date_fin = timezone.now() + relativedelta(months=1)
    etat= None
    for k, v in dict(SuiviLoyer.ETAT).items():
        if k == str('A_VERIFIER'):
            etat = str(k)
    suivis = SuiviLoyer.find_suivis_a_verifier(date_debut,date_fin)
    # suivis=None
    return render(request, 'myhome.html',
                        {'alertes':    Alerte.find_by_etat_today('A_VERIFIER'),
                         'batiments' : Batiment.find_my_batiments(),
                         'contrats' :  ContratGestion.find_my_contrats(),
                         'suivis'    : suivis})


def listeBatiments(request):
    batiments = Batiment.objects.all()
    return render(request, 'listeBatiments.html', {'batiments': batiments})

def listeBatiments_filtrer(request, personne_id):
    print('listeBatiments_filtrer')
    personne = None
    if personne_id is None:
        batiments = Batiment.objects.all()
    else:
        personne = Personne.objects.get(id=personne_id)
        batiments = personne.batiments

    return render(request, 'listeBatiments.html', {'batiments': batiments,
                                                   'filtre': personne})

@login_required
def listePersonnes(request):
    personnes = Personne.objects.all()
    return render(request, 'listePersonnes.html', {'personnes': personnes})

@login_required
def listeComplete(request):
    batiments = Batiment.objects.all()
    contrats_location = ContratLocation.objects.all()
    return render(request, 'listeComplete.html', {'batiments': batiments})

def alertes4(request):
    batiment = Batiment.objects.get(nom='batiment 5b')
    proprietaires = Proprietaire.objects.filter(batiment=batiment)

    return render(request, 'main/alertes4.html', {'batiment' : batiment,'proprietaires': proprietaires})


@login_required
def personne(request, personne_id):
    personne = Personne.find_personne(personne_id)
    return render(request, "personne_form.html",
                  {'personne':         personne})


def update_personne(request):
    print('update_personne')

    personne = Personne()
    print(request.POST['action'])
    if ('add' == request.POST['action'] or 'modify' == request.POST['action']):
        print(request.POST['id'])
        personne = get_object_or_404(Personne, pk=request.POST['id'])
        personne.nom = request.POST['nom']
        personne.prenom = request.POST['prenom']

        personne.save()


    return render(request, "personne_form.html",
                  {'personne':         personne})


def xlsRead(request):
    short_description = u"Export XLS"


class BatimentDetailView(DetailView):
    model = Batiment

    def get_context_data(self, **kwargs):
        context = super(BatimentDetailView, self).get_context_data(**kwargs)
        return context

class FraisMaintenanceDetail(DetailView):
    model= FraisMaintenance

class FraisMaintenanceCreate(CreateView):
    model=FraisMaintenance;
    form_class = FraisMaintenanceForm

class FraisMaintenanceUpdate(UpdateView):
    model=FraisMaintenance;
    form_class = FraisMaintenanceForm

class FraisMaintenanceDelete(DeleteView):
    model=FraisMaintenance;
    success_url = reverse_lazy('fraismaintenance-list'),

class PersonneList(ListView):
    model = Personne

class PersonneDetail(DetailView):
    model= Personne

class PersonneCreate(CreateView):
    model=Personne;
    form_class = PersonneForm

class PersonneUpdate(UpdateView):
    model=Personne;
    form_class = PersonneForm

class PersonneDelete(DeleteView):
    model=Personne;
    success_url="../../../personnes"

class BatimentList(ListView):
    model = Batiment

class BatimentCreate(CreateView):
    model=Batiment;
    form_class = BatimentForm

class BatimentUpdate(UpdateView):
    model=Batiment;
    form_class = BatimentForm

class BatimentDelete(DeleteView):
    model=Batiment;
    success_url="../../../batiments"

class ProprietaireList(ListView):
    model = Proprietaire

class ProprietaireDetail(DetailView):
    model= Proprietaire

class ProprietaireCreate(CreateView):
    model=Proprietaire;
    form_class =ProprietaireForm

    def form_valid(self, form):
        print('form valid')
        proprietaire = form.save(commit=False)
        # article.author = self.request.user
        return super(ProprietaireCreate, self).form_valid(form)

class ProprietaireCreateForBatiment(CreateView):
    model=Proprietaire;
    form_class =ProprietaireForm
    def get_initial(self):
        initial_data = super(ProprietaireCreateForBatiment, self)\
                            .get_initial()
        course = get_object_or_404(Batiment, pk=self.kwargs['pk'])
        if course:
            initial_data['batiment']=course
        # if self.form_class == TransferFormFrom:
        #     initial_data['from_account'] = self.acct_pk
        # elif self.form_class == TransferFormTo:
        #     initial_data['to_account'] = self.acct_pk
        # else:
        #     raise ImproperlyConfigured(
        #                 '"form_class" variable must be defined '
        #                 'in %s for correct initial behavior.'
        #                 % (self.__class__.__name__,
        #                    obj.__class__.__name__))
        return initial_data
    # def get_form(self, form_class):
    #     form = super(ProprietaireCreateForBatiment, self).get_form(form_class)
    #     course = get_object_or_404(Batiment, pk=self.kwargs['pk'])
    #
    #     form.instance.batiment = course
    #     print (course)
    #     # return form
    #     return super(ProprietaireCreateForBatiment, self).form_valid(form)
    # def form_valid(self, form):
    #     print('kkk')
    #     print(self.kwargs['pk'])
    #     form.instance.batiment = get_object_or_404(Event,
    #                                             pk=self.kwargs['pk'])
    #     return super(ProprietaireCreateForBatiment, self).form_valid(form)
    # def get_form_class(self):
    #     return ProprietaireForm
    #
    # def get_form_kwargs(self, **kwargs):
    #     print('get_form_kwargs')
    #     kwargs = super(ProprietaireCreateForBatiment, self).get_form_kwargs(**kwargs)
    #     print (kwargs)
    #     if 'pk' in kwargs:
    #         print(self.kwargs['pk'])
    #         batiment = Batiment.objects.get(pk=self.kwargs['pk'])
    #         instance = Proprietaire(batiment=batiment)
    #         kwargs.update({'instance': instance})
    #     else:
    #         print('les')
    #     return
    #
    def form_valid(self, form):
        print('form valid')
        proprietaire = form.save(commit=False)
        # article.author = self.request.user
        return super(ProprietaireCreateForBatiment, self).form_valid(form)
    #
    # def dispatch(self, request, *args, **kwargs):
    #     print('displath')
    #     self.batiment = Batiment.objects.get(pk=self.kwargs['pk'])
    #     print (self.batiment)
    #
    #     return super(ProprietaireCreateForBatiment, self).dispatch(request, *args, **kwargs)

    #
    # def form_valid(self, form):
    #     print('form_valid')
    #     form.instance.batiment= self.batiment
    #     return super(ProprietaireCreateForBatiment, self).form_valid(form)

    #
    # form_class = ProprietaireForm
    # batiment = Batiment.objects.get(pk=1)
    # form_class.batiment = batiment
    # # fields = ['batiment']
    #
    # def form_valid(self, form):
    #     print('form_valid')
    #     form.instance.batiment = Batiment.objects.get(pk=self.kwargs['class'])
    #     # event = Event.objects.get(pk=self.kwargs['class'])
    #     return super(ProprietaireCreateForBatiment, self).form_valid(form)

class ProprietaireUpdate(UpdateView):
    model=Proprietaire;
    form_class = ProprietaireForm

class ProprietaireDelete(DeleteView):
    model=Proprietaire;
    success_url="../../../proprietaires"



class SocieteList(ListView):
    model = Societe

class SocieteDetail(DetailView):
    model= Societe

class SocieteCreate(CreateView):
    model=Societe;
    form_class = SocieteForm

class SocieteUpdate(UpdateView):
    model=Societe;
    form_class = SocieteForm

class SocieteDelete(DeleteView):
    model=Societe;
    success_url="../../../societes"



# class ContratLocationList(ListView):
#     model = ContratLocation
#
# class ContratLocationDetail(DetailView):
#     model= ContratLocation
#
#
# class ContratLocationUpdate(UpdateView):
#     print('ContratLocationUpdate')
#     model=ContratLocation
#     form_class = ContratLocationForm
#
# class ContratLocationDelete(DeleteView):
#     model=ContratLocation
#     success_url="../../../batiments"
#
# class ContratLocationCreate(CreateView):
#     model=ContratLocation
#     form_class =ContratLocationForm
#
#     def get_initial(self):
#         print('initiale')
#         if self.kwargs:
#             initial_data = super(ContratLocationCreate, self)\
#                                 .get_initial()
#             batiment = get_object_or_404(Batiment, pk=self.kwargs['pk'])
#             location = get_object_or_404(ContratLocation, pk=batiment.location_actuelle.id)
#
#             if batiment:
#                 initial_data['batiment']=batiment
#                 initial_data['date_debut']=location.date_fin
#                 initial_data['date_fin']=location.date_fin + relativedelta(years=1)
#                 initial_data['loyer_base']=location.loyer_base
#                 initial_data['charges_base']=location.charges_base
#                 initial_data['action']='ddd'
#
#                 form_class.action ='kkk'
#             return initial_data
