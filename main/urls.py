##############################################################################
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
from . import views, batiment, proprietaire, suivis, contratlocation, financement, locataire, contratgestion, \
    frais, honoraire, personne, essai_pdf, assurance, pays, fonction, societe, document,\
    lettre
from main import alertes
from main.pdf import image
from django.conf.urls import url
from django.contrib.auth.views import login, logout
from django.conf import settings


urlpatterns = [
    url(r'^$', views.home, name='home'),
    # login / logout urls
    url(r'^login/$',login, {'template_name': settings.LOGOUT_REDIRECT_URL}, name='login'),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    # listes
    url(r'^listeComplete', views.listeComplete),
    url(r'^listeBatiments', views.listeBatiments, name='listeBatiments'),

    url(r'^listeProprietaires', proprietaire.liste_proprietaires, name='listeProprietaires'),
    url(r'^listeContratGestion/$', views.ContratGestionList.as_view(), name='contrat_gestion_list'),
    url(r'^contratGestion/(?P<pk>[0-9]+)/$', views.ContratGestionDetail.as_view(), name='contrat_gestion_detail'),
    # ecran de detail
    url(r'^batiment/([0-9]+)/$', batiment.batiment_form, name='batiment'),
    url(r'^proprietaire/([0-9]+)/$', proprietaire.proprietaire, name='proprietaire'),
    url(r'^proprietaire/update/([0-9]+)/$', proprietaire.update_proprietaire, name='update_proprietaire'),
    url(r'^proprietaire/delete/([0-9]+)/$', proprietaire.delete_proprietaire, name='delete_proprietaire'),
    url(r'^proprietaire/dadd/([0-9]+)/$', proprietaire.add_proprietaire, name='add_proprietaire'),
    url(r'^proprietaire/$', proprietaire.proprietaire_update_save, name='proprietaire-update-save'),
    url(r'^proprietaire/createb/([0-9]+)/$', proprietaire.proprietaire_create_for_batiment,
        name='proprietaire-create-batiment'),

    # old
    # url(r'^suivis/$', suivis.suivis, name='suivis'),
    # url(r'^suivis/refresh/$', suivis.refresh_suivis, name='refresh_suivis'),
    url(r'^suivis/$', suivis.suivis, name='suivis'),
    url(r'^suivis/search$', suivis.suivis_search, name='suivis_search'),
    url(r'^suivis/update$', suivis.suivis_update, name='suivis-update'),
    # url(r'^suivis/updatel/([0-9]+)/$', suivis.suivis_updatel, name='suivis-updatel'),
    url(r'^suivis/updatel/([0-9]+)/liste/$', suivis.suivis_update_liste, name='suivis-update-liste'),
    url(r'^suivis/updatel/([0-9]+)/home/$', suivis.suivis_update_home, name='suivis-update-home'),
    url(r'^suivis/updatel/([0-9]+)/location/$', suivis.suivis_update_location, name='suivis-update-location'),

    url(r'^suivis/update_suivi$', suivis.update_suivi, name='update_suivi'),


    # url(r'^update_personne/$', views.update_personne, name='update_personne'),
    url(r'^update_batiment/$', batiment.update, name='update_batiment'),

    # url(r'^photos/(?P<path>.*)$', 'django.views.static.serve', {
    #         'document_root': settings.MEDIA_ROOT,
    #     }),

    url(r'^fraismaintenances/$', frais.list, name='fraismaintenance_list'),
    url(r'^fraismaintenance/new/$', frais.new, name='fraismaintenance-new'),
    url(r'^fraismaintenance/create/([0-9]+)/$', frais.create, name='fraismaintenance-create'),
    url(r'^fraismaintenance/prepare/update/([0-9]+)/$', frais.prepare_update, name='fraismaintenance-prepare-update'),
    url(r'^fraismaintenance/update/$', frais.update, name='fraismaintenance-update'),
    url(r'^fraismaintenance/delete/([0-9]+)/$', frais.delete_frais, name='fraismaintenance-delete'),
    url(r'^fraismaintenance/(?P<pk>[0-9]+)/$', views.FraisMaintenanceDetail.as_view(), name='fraismaintenance_detail'),

    url(r'^personne/create/$', personne.create, name='personne-create'),
    url(r'^personne/create/locataire/$', locataire.personne_create, name='personne-create-locataire'),
    url(r'^personne/create/proprietaire/$', proprietaire.personne_create, name='personne-create-proprietaire'),

    url(r'^personne/edit/([0-9]+)/$', personne.edit, name='personne-edit'),
    url(r'^personne/update/$', personne.update, name='personne-update'),
    url(r'^personne/delete/(?P<pk>[0-9]+)/$', views.PersonneDelete.as_view(), name='personne-delete'),
    url(r'^personne/delete2/([0-9]+)/$', views.personne_delete, name='personne-delete-2'),
    url(r'^personnes/$', personne.list, name='personne_list'),
    url(r'^personnes/search/$', personne.search, name='personne_search'),
    url(r'^validate_personne/$', personne.validate_personne, name='validate_personne'),

    url(r'^batiment/create/$', batiment.create, name='batiment-create'),
    url(r'^batiment/([0-9]+)/$', batiment.batiment_form, name='batiment'),
    url(r'^batiment/update/([0-9]+)/$', batiment.update, name='batiment-update'),
    url(r'^batiment/delete/([0-9]+)/$', batiment.delete, name='batiment-delete'),
    url(r'^batiments/$', views.BatimentList.as_view(), name='batiment_list'),
    url(r'^batiment/deletep/([0-9]+)/$', proprietaire.delete_proprietaire_batiment,
        name='delete_proprietaire_batiment'),
    url(r'^batiment/fraismaintenance/prepare/update/([0-9]+)/$', frais.prepare_update_from_batiment, name='fraismaintenance-edit-from-batiment'),
    url(r'^location/fraismaintenance/prepare/update/([0-9]+)/$', frais.prepare_update_from_location, name='fraismaintenance-edit-from-location'),
    url(r'^dashboard/fraismaintenance/prepare/update/([0-9]+)/$', frais.prepare_update_from_dashboard, name='fraismaintenance-edit-from-dashboard'),
    url(r'^frais/list/fraismaintenance/prepare/update/([0-9]+)/$', frais.prepare_update_from_list, name='fraismaintenance-edit-from-list'),

    url(r'^batiment/fraismaintenance/delete/([0-9]+)/$', frais.delete_frais_from_batiment, name='fraismaintenance-delete-from-batiment'),
    url(r'^location/fraismaintenance/delete/([0-9]+)/$', frais.delete_frais_from_location, name='fraismaintenance-delete-from-location'),
    url(r'^frais/liste/fraismaintenance/delete/([0-9]+)/$', frais.delete_frais_from_list, name='fraismaintenance-delete-from-list'),
    # url(r'^proprietaire/create/$', views.ProprietaireCreate.as_view(), name='proprietaire-create'),
    # url(r'^proprietaire/createb/(?P<pk>[0-9]+)/$', views.ProprietaireCreateForBatiment.as_view(), name='proprietaire-create-batiment'),
    # url(r'^proprietaire/update/(?P<pk>[0-9]+)/$', views.ProprietaireUpdate.as_view(), name='proprietaire-update'),
    # url(r'^proprietaire/delete/(?P<pk>[0-9]+)/$', views.ProprietaireDelete.as_view(), name='proprietaire-delete'),
    # url(r'^proprietaires/$', views.ProprietaireList.as_view(), name='proprietaire_list'),
    # url(r'^proprietaire/(?P<pk>[0-9]+)/$', views.ProprietaireDetail.as_view(), name='proprietaire_detail'),
    url(r'^contratgestion/new/$', contratgestion.new, name='contratgestion-new'),
    url(r'^contratgestion/create/([0-9]+)/$', contratgestion.create, name='contratgestion-create'),
    # url(r'^contratgestion/update/(?P<pk>[0-9]+)/$', views.ContratGestionUpdate.as_view(), name='contratgestion-update'),
    url(r'^contratgestion/delete/([0-9]+)/$', contratgestion.delete, name='contratgestion-delete'),
    url(r'^gestion/prepare/update/all/([0-9]+)/$', contratgestion.prepare_update, name='gestion-prepare-update-all'),
    url(r'^gestion/update/all/$', contratgestion.update, name='update-gestion-all'),
    url(r'^contratgestion/form/(?P<id_contrat>[0-9]+)/$', contratgestion.saveupdate, name='gestion-create-update'),



    url(r'^contratgestions/$', contratgestion.list, name='contratgestion_list'),

    # url(r'^contratgestion/(?P<pk>[0-9]+)/$', views.ContratGestionDetail.as_view(), name='contratgestion'),

    url(r'^societe/delete/(?P<pk>[0-9]+)/$', views.SocieteDelete.as_view(), name='societe-delete'),
    url(r'^societes/$', societe.list, name='societe-list'),
    url(r'^societe/(?P<pk>[0-9]+)/$', views.SocieteDetail.as_view(), name='societe'),
    url(r'^societe/create/personne/$', societe.create, name='personne-create-societe'),
    # url(r'^batiment5/(?P<pk>\d+)/$', BatimentDetailView.as_view(), batiment_info)
    url(r'^alertes/$', alertes.list, name='alerte-list'),
    url(r'^alertes/update/$', alertes.update_a_verifier, name='alerte-update-a-verifier'),
    url(r'^alertes/search/$', alertes.search, name='alerte-search'),

    # url(r'^location/create/$', views.ContratLocationCreate.as_view(), name='location-create'),
    # url(r'^location/update/(?P<pk>[0-9]+)/$', views.ContratLocationUpdate.as_view(), name='location-update'),

    url(r'^location/prepare/update/all/([0-9]+)/$', contratlocation.prepare_update, name='location-prepare-update-all'),
    url(r'^location/update/all/$', contratlocation.update, name='update-location-all'),
    url(r'^location/createb/([0-9]+)/$', contratlocation.contrat_location_for_batiment,
        name='location-create-batiment'),
    url(r'^location/createl/$', contratlocation.test, name='add-location-for-batiment'),

    url(r'^location/delete/([0-9]+)/$', contratlocation.delete, name='location-delete'),
    # url(r'^location/(?P<pk>[0-9]+)/$', views.ContratLocationDetail.as_view(), name='contratlocation_detail'),
    # url(r'^contratlocations/$', views.ContratLocationList.as_view(), name='contratlocation_list'),
    url(r'^contratlocations/$', contratlocation.list, name='contratlocation_list'),


    url(r'^financement/new/([0-9]+)/$', financement.new, name='financement-new'),
    url(r'^financement/create/$', financement.create, name='create-financement'),
    url(r'^locataire/new/([0-9]+)/$', locataire.new, name='locataire-new'),
    url(r'^locataire/all/new/$', locataire.new_without_known_location, name='locataire-new-location'),
    url(r'^locataire/add/$', locataire.add, name='locataire-add'),
    url(r'^locataire/delete/([0-9]+)/$', locataire.delete, name='locataire-delete'),
    url(r'^locataires/$', locataire.list, name='locataire-list'),
    url(r'^locataire/([0-9]+)/$', locataire.locataire_form, name='locataire'),
    url(r'^locataire/update/([0-9]+)/$', locataire.update, name='locataire-update'),

    url(r'^honoraires/$', honoraire.list, name='honoraire-list'),
    url(r'^honoraires/search/$', honoraire.search, name='honoraires-search'),
    url(r'^honoraire/update/$', honoraire.update, name='honoraire-update'),
    url(r'^honoraire/edit/([0-9]+)/$', honoraire.honoraire_form, name='honoraire'),
    url(r'^honoraire/delete/(?P<pk>[0-9]+)/$', views.HonoraireDelete.as_view(), name='honoraire-delete'),
    url(r'^test/$', views.merge_form, name='test'),
    url(r'^test/image/$', image.test_image, name='test_image'),
    url(r'^test/merge/$', views.test_merge, name='test_merge'),
    url(r'^test/upload/$', image.upload, name='upload'),
    url(r'^test/upload2/$', essai_pdf.test_create_pdf, name='test_pdf'),
    # url(r'^test3/$', essai3.test, name='test3'),

    url(r'^assurance_create/$', assurance.create, name='assurance_create'),
    url(r'^prolongation/$', contratlocation.prolongation, name='prolongation'),
    url(r'^fonction_create/$', fonction.create, name='fonction_create'),
    url(r'^societes_liste/$', societe.societe_liste, name='societe_liste'),
    url(r'^batiment/search/$', batiment.search_par_proprietaire, name='batiment_search'),
    url(r'^societe/update/$', societe.update, name='societe_update'),
    url(r'^societe/edit/pl/([0-9]+)/$', societe.societe_edit_from_person_list, name='societe_edit_from_person_list'),
    url(r'^societe/edit/sl/([0-9]+)/$', societe.societe_edit_from_list, name='societe_edit_from_list'),

    url(r'^location/form/$', contratlocation.contrat_location_form, name="contrat_location_form"),
    url(r'^location/search/$', contratlocation.search, name='location_search'),
    url(r'^fraismaintenance/contrat/new/([0-9]+)/$', frais.contrat_new, name='fraismaintenance-new-contrat'),

    url(r'^test/lettre/$', views.lettre_form, name='lettre'),
    url(r'^test/lettre_create/$', lettre.lettre_create, name='lettre_create'),
    url(r'^pays_create/$', pays.create, name='pays_create'),

    url(r'^societe_create/$', societe.create_new, name='societe_create'),
    url(r'^document/liste/$', document.document_bd_list, name='document_list'),
    url(r'^document/form/([0-9]+)/$', document.document_form, name='document_form'),
    url(r'^document/lettre_indexation_form/([0-9]+)/$', document.lettre_indexation_form, name='lettre_indexation_form'),
    url(r'^document/lettre_indexation_new/([0-9]+)/$', document.lettre_indexation_new, name='lettre_indexation_new'),
    url(r'^document/lettre_indexation/([0-9]+)/$', document.lettre_indexation, name='lettre_indexation'),
    url(r'^manuel/$', views.manuel, name='manuel'),
    url(r'^check_societe/$', societe.check_societe, name='check_societe'),


]
