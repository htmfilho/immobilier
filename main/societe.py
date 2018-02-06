##############################################################################
#
#    Immobilier it's an application
#    designed to manage the core business of property management, buildings,
#    rental agreement and so on.
#
#    Copyright (C) 2016-2017 Verpoorten Leïla
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
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from main import models as mdl
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from main.models.enums.type_societe import TYPE_SOCIETE


NEXT_NAV_SOCIETE_LIST  = 'societe_list'
NEXT_NAV_PERSONNE_LIST  = 'person_list'

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class SocieteSerializer(serializers.ModelSerializer):

    class Meta:
        model = mdl.societe.Societe
        fields = '__all__'


def societe_liste(request):
    return render(request, 'liste_societes.html', {'societes': mdl.societe.find_all()})


def update(request):

    societe_id = None
    if request.POST['societe_id']:
        societe_id = int(request.POST['societe_id'])
    societe = get_societe(societe_id)

    societe.nom = request.POST['nom']
    societe.description = request.POST['description']
    societe.rue = request.POST['rue']
    if request.POST['numero'] != '':
        societe.numero = request.POST['numero']
    else:
        societe.numero = None
    societe.boite = request.POST['boite']
    societe.lieu_dit = request.POST['lieu_dit']
    societe.localite = None
    if request.POST['localite']:
        if request.POST['localite'] != '':
            societe.localite = mdl.localite.find_by_id(int(request.POST['localite']))

    societe.save()
    return redirection_next_nav(request.POST.get('next_nav', None))


def redirection_next_nav(next_nav):
    if next_nav == NEXT_NAV_SOCIETE_LIST:
        return HttpResponseRedirect(reverse('societe-list'))

    elif next_nav == NEXT_NAV_PERSONNE_LIST:
        return HttpResponseRedirect(reverse('personne_list'))
    else:
        return HttpResponseRedirect(reverse('home'))


def get_societe(societe_id):
    if societe_id:
        return get_object_or_404(mdl.societe.Societe, pk=societe_id)
    else:
        return mdl.societe.Societe()


def societe_edit_from_list(request, societe_id):
    return societe_edit(request, societe_id, NEXT_NAV_SOCIETE_LIST)


def societe_edit_from_person_list(request, societe_id):
    return societe_edit(request, societe_id, NEXT_NAV_PERSONNE_LIST)


def societe_edit(request, societe_id,next_nav):
    societe = get_societe(societe_id)
    return render(request, "societe_form.html",
                  {'societe': societe,
                   'localites': mdl.localite.find_all(),
                   'type': 'from_person',
                   'next_nav': next_nav})


def create(request):
    id_personne = request.POST.get('id_pers', None)
    societe = mdl.societe.Locataire(nom=request.POST.get('nom_societe', None))
    societe.save()
    if id_personne:
        personne = get_object_or_404(mdl.personne.Personne, pk=id_personne)
    return HttpResponseRedirect(reverse('personne-edit', args=(personne.id, )))


def create_new(request):
    nouvelle_societe = populate_societe(request)
    nouvelle_societe.save()

    serializer = SocieteSerializer(mdl.societe.find_all(), many=True)
    return JSONResponse(serializer.data)


def populate_societe(request):
    nom_societe = request.GET.get('nom', None)
    nouvelle_societe = None
    if nom_societe:
        nouvelle_societe = mdl.societe.Societe()
        nouvelle_societe.nom = request.GET.get('nom', None)
        nouvelle_societe.description = request.GET.get('description', None)
        nouvelle_societe.rue = request.GET.get('rue', None)
        try:
            nouvelle_societe.numero = int(request.GET.get('numero', None))
        except:
            nouvelle_societe.numero = None
        nouvelle_societe.boite = request.GET.get('boite', None)
        localite_nom = request.GET.get('localite', None)
        localite_cp = request.GET.get('localite_cp', None)
        nouvelle_societe.localite = None
        print(localite_cp)
        if localite_nom or localite_cp:
            localite = mdl.localite.search(localite_cp, localite_nom).first()
            if localite:
                nouvelle_societe.localite = localite
            else:
                nouvelle_societe.localite = mdl.localite.create_localite(localite_nom, localite_cp)

        type_societe = request.GET.get('type', None)

        nouvelle_societe.type = None
        if type_societe:
            nouvelle_societe.type =  mdl.type_societe.find_by_id(type_societe)
            print(nouvelle_societe.type)
    return nouvelle_societe


def creation_nouvelle_societe(new_value, a_description=None):
    societe = mdl.societe.Societe(nom=new_value,
                                  description=a_description)
    societe.save()
    return societe


def list(request):
    return render(request, "societe/societe_list.html",
                  {'societes': mdl.societe.find_all()})


def check_societe(request):
    nom = request.GET.get('nom', None)
    if nom:
        results = mdl.societe.find_name(nom)
        serializer = SocieteSerializer(results, many=True)
        return JSONResponse(serializer.data)
    return None