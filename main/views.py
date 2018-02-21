#############################################################################
#
#    Immobilier it's an application
#    designed to manage the core business of property management, buildings,
#    rental agreement and so on.
#
#    Copyright (C) 2016-2018 Verpoorten Leïla
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from django.contrib.auth.decorators import login_required
from main import models as mdl
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import *
from django.core.urlresolvers import reverse_lazy
from main.forms.forms import BatimentForm, ProprietaireForm, FraisMaintenanceForm, SocieteForm, LettreForm, LigneForm

from reportlab.lib.units import mm

from reportlab.lib.pagesizes import A4 as A4
import datetime

from django.forms import formset_factory
from main.pages_utils import PAGE_LISTE_BATIMENTS
from main.models.enums import etat_honoraire
from main.pdf import merge_pdf
from django.http import FileResponse, Http404
import re
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

ZERO = 0


class ContratGestionList(ListView):
    model = mdl.contrat_gestion


class ContratGestionDetail(DetailView):
    model = mdl.contrat_gestion


class FraisMaintenanceList(ListView):
    model = mdl.frais_maintenance


class FraisMaintenanceDetail(DetailView):
    model = mdl.frais_maintenance


@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html', {})


@login_required
def home(request):
    suivis = mdl.suivi_loyer.find_suivis_a_verifier_proche()

    suivis_recus = mdl.suivi_loyer.find_mes_suivis_by_etat_suivi(timezone.now(), 'PAYE')
    suivis_non_paye = mdl.suivi_loyer.find_suivis_by_pas_etat_suivi(timezone.now(), 'PAYE')
    montant_recu = 0
    montant_attendu = 0
    mois_en_cours = str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().year)
    mes_frais = mdl.frais_maintenance.find_mes_frais_du_mois()

    return render(request, 'myhome.html',
                  {'alertes':         mdl.alerte.find_by_etat_today('A_VERIFIER'),
                   'batiments':       mdl.batiment.find_batiments_gestionnaire(),
                   'contrats':        mdl.contrat_gestion.find_my_contrats(),
                   'honoraires':      mdl.honoraire.find_honoraires_by_etat_today(etat_honoraire.A_VERIFIER),
                   'suivis':          suivis,
                   'previous':        request.POST.get('previous', None),
                   'suivis_recus':    suivis_recus,
                   'montant_recu':    montant_recu,
                   'montant_attendu': montant_attendu,
                   'suivis_non_paye': suivis_non_paye,
                   'locataires':      mdl.locataire.find_my_locataires(),
                   'mois_en_cours':   mois_en_cours,
                   'mes_frais':       mes_frais,
                   'tot_depenses':    _get_total_depenses(mes_frais),
                   'tot_recettes':    _get_total_recettes(suivis_recus)})


def _get_total_depenses(mes_frais):
    tot_depenses = ZERO
    if mes_frais:
        for f in mes_frais:
            tot_depenses += _get_montant_to_add(f.montant)
    return tot_depenses


def _get_total_recettes(suivis_recus):
    tot_recettes = ZERO
    if suivis_recus:
        for s in suivis_recus:
            tot_recettes += _get_montant_to_add(s.loyer_percu)
            tot_recettes += _get_montant_to_add(s.charges_percu)
    return tot_recettes


def _get_montant_to_add(sum):
    if sum:
        return sum
    return ZERO


@login_required
def listeBatiments(request):
    batiments = mdl.batiment.find_all()
    return render(request, PAGE_LISTE_BATIMENTS,
                  {'batiments': batiments,
                   'proprietaires': mdl.proprietaire.find_distinct_proprietaires()})


@login_required
def listeComplete(request):
    batiments = mdl.batiment.find_all()
    return render(request, 'listeComplete.html', {'batiments': batiments})


@login_required
def personne(request, personne_id):
    une_personne = mdl.personne.find_personne(personne_id)
    return render(request, "personne/personne_form.html",
                  {'personne': une_personne,
                   'societes': mdl.societe.find_all()})


def update_personne(request):
    une_personne = mdl.personne.Personne()
    if 'add' == request.POST.get('action', None) or 'modify' == request.POST.get('action', None):
        une_personne = get_object_or_404(mdl.personne.Personne, pk=request.POST['id'])
        une_personne.nom = request.POST['nom']
        une_personne.prenom = request.POST['prenom']

        une_personne.save()
    return render(request, "personne/personne_form.html",
                  {'personne': une_personne,
                   'societes': mdl.societe.find_all()})


class FraisMaintenanceCreate(CreateView):
    model = mdl.frais_maintenance
    form_class = FraisMaintenanceForm


class FraisMaintenanceUpdate(UpdateView):
    model = mdl.frais_maintenance
    form_class = FraisMaintenanceForm


class FraisMaintenanceDelete(DeleteView):
    model = mdl.frais_maintenance
    success_url = reverse_lazy('fraismaintenance-list'),


class PersonneDelete(DeleteView):
    model = mdl.personne
    success_url = "../../../personnes"


class BatimentList(ListView):
    model = mdl.batiment


class BatimentCreate(CreateView):
    model = mdl.batiment
    form_class = BatimentForm


class BatimentUpdate(UpdateView):
    model = mdl.batiment
    form_class = BatimentForm


class BatimentDelete(DeleteView):
    model = mdl.batiment
    success_url = "../../../batiments"


class ProprietaireList(ListView):
    model = mdl.proprietaire


class ProprietaireDetail(DetailView):
    model = mdl.proprietaire


class ProprietaireCreate(CreateView):
    model = mdl.proprietaire
    form_class = ProprietaireForm

    def form_valid(self, form):
        form.save(commit=False)
        return super(ProprietaireCreate, self).form_valid(form)


class ProprietaireCreateForBatiment(CreateView):
    model = mdl.proprietaire
    form_class = ProprietaireForm

    def get_initial(self):
        initial_data = super(ProprietaireCreateForBatiment, self).get_initial()
        course = get_object_or_404(mdl.batiment.Batiment, pk=self.kwargs['pk'])
        if course:
            initial_data['batiment'] = course
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
    #     course = get_object_or_404(mdl.batiment.Batiment, pk=self.kwargs['pk'])
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
    #         batiment = mdl.batiment.objects.get(pk=self.kwargs['pk'])
    #         instance = Proprietaire(batiment=batiment)
    #         kwargs.update({'instance': instance})
    #     else:
    #         print('les')
    #     return
    #

    def form_valid(self, form):
        form.save(commit=False)
        # article.author = self.request.user
        return super(ProprietaireCreateForBatiment, self).form_valid(form)
    #
    # def dispatch(self, request, *args, **kwargs):
    #     print('displath')
    #     self.batiment = mdl.batiment.objects.get(pk=self.kwargs['pk'])
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
    # batiment = mdl.batiment.objects.get(pk=1)
    # form_class.batiment = batiment
    # # fields = ['batiment']
    #
    # def form_valid(self, form):
    #     print('form_valid')
    #     form.instance.batiment = mdl.batiment.objects.get(pk=self.kwargs['class'])
    #     # event = Event.objects.get(pk=self.kwargs['class'])
    #     return super(ProprietaireCreateForBatiment, self).form_valid(form)


class ProprietaireUpdate(UpdateView):
    model = mdl.proprietaire
    form_class = ProprietaireForm


class ProprietaireDelete(DeleteView):
    model = mdl.proprietaire
    success_url = "../../../proprietaires"


class SocieteDetail(DetailView):
    model = mdl.societe


class SocieteCreate(CreateView):
    model = mdl.societe
    form_class = SocieteForm


class SocieteUpdate(UpdateView):
    model = mdl.societe
    form_class = SocieteForm


class SocieteDelete(DeleteView):
    model = mdl.societe
    success_url = "../../../societes"


class HonoraireDelete(DeleteView):
    model = mdl.honoraire
    success_url = "../../../honoraires"


def test_merge(request):
    return merge_pdf.merge(request)


def merge_form(request):
    return render(request, "test.html")


def personne_delete(request, id):
    mdl.personne.delete_personne(int(id))
    return HttpResponseRedirect(reverse('personne_search'))


def lettre_form(request):
    modele = mdl.modele_document.find_by_reference('LETTRE_INDEXATION')
    form = None
    formset = None
    if request.method == 'POST':
        pass
    else:
        ArticleFormSet = formset_factory(LigneForm, extra=2)
        formset = ArticleFormSet(initial=[{'test': 'Django is now open source', },
                                          {'test': 'Django is now open source2', }])

        form = LettreForm(initial={'sujet': modele.sujet, 'format': "docx", 'fichier_modele': modele.fichier_modele,
                                   'titre': 'Monsieur',
                                   'tableSet': formset})
    return render(request, "lettre.html", {'form': form, 'formset': formset})


def manuel(request):
    try:
        return FileResponse(open('doc/manuel.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()
