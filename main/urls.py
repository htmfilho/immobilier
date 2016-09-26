from django.conf import settings
from . import views, batiment, proprietaire, suivis, alertes, contratlocation, financement, locataire, contratgestion, \
    frais, honoraire, personne, tests, test3, assurance
from django.conf.urls import url
from django.contrib.auth.views import login,logout

urlpatterns = [
    url(r'^$', views.home, name='home'),
    # login / logout urls
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    # listes
    url(r'^listeComplete', views.listeComplete),
    url(r'^listeBatiments', views.listeBatiments, name='listeBatiments'),
    url(r'^listeBatiments/filtrer/personne/([0-9]+)/$', views.listeBatiments_filtrer, name='listeBatiments-filtrer-personne'),

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
    url(r'^proprietaire/createb/([0-9]+)/$', proprietaire.proprietaire_create_for_batiment, name='proprietaire-create-batiment'),

    #old
    # url(r'^suivis/$', suivis.suivis, name='suivis'),
    # url(r'^suivis/refresh/$', suivis.refresh_suivis, name='refresh_suivis'),
    url(r'^suivis/$', suivis.suivis, name='suivis'),
    url(r'^suivis/search$', suivis.suivis_search, name='suivis_search'),
    url(r'^suivis/update$', suivis.suivis_update, name='suivis-update'),
    url(r'^suivis/updatel/([0-9]+)/$', suivis.suivis_updatel, name='suivis-updatel'),
    url(r'^suivis/update_suivi$', suivis.update_suivi, name='update_suivi'),


    # url(r'^update_personne/$', views.update_personne, name='update_personne'),
    url(r'^update_batiment/$', batiment.update, name='update_batiment'),

    # test
    url(r'^xlsRead', views.xlsRead, name='xlsRead'),

    url(r'^photos/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    url(r'^test4', views.alertes4),

    url(r'^fraismaintenances/$', frais.list, name='fraismaintenance_list'),
    url(r'^fraismaintenance/new/$', frais.new, name='fraismaintenance-new'),
    url(r'^fraismaintenance/create/([0-9]+)/$', frais.create, name='fraismaintenance-create'),
    url(r'^fraismaintenance/prepare/update/([0-9]+)/$', frais.prepare_update, name='fraismaintenance-prepare-update'),
    url(r'^fraismaintenance/update/$', frais.update, name='fraismaintenance-update'),
    url(r'^fraismaintenance/delete/(?P<pk>[0-9]+)/$', views.FraisMaintenanceDelete.as_view(), name='fraismaintenance-delete'),
    url(r'^fraismaintenance/(?P<pk>[0-9]+)/$', views.FraisMaintenanceDetail.as_view(), name='fraismaintenance_detail'),

    url(r'^personne/create/$', personne.create, name='personne-create'),
    url(r'^personne/create/locataire/$', locataire.personne_create, name='personne-create-locataire'),
    url(r'^personne/create/proprietaire/$', proprietaire.personne_create, name='personne-create-proprietaire'),

    url(r'^personne/edit/([0-9]+)/$', personne.edit, name='personne-edit'),
    url(r'^personne/update/$', personne.update, name='personne-update'),
    url(r'^personne/delete/(?P<pk>[0-9]+)/$', views.PersonneDelete.as_view(), name='personne-delete'),
    url(r'^personnes/$', personne.list, name='personne_list'),
    url(r'^personnes/search/$', personne.search, name='personne_search'),


    url(r'^batiment/create/$', batiment.create, name='batiment-create'),
    url(r'^batiment/([0-9]+)/$', batiment.batiment_form, name='batiment'),
    url(r'^batiment/update/([0-9]+)/$', batiment.update, name='batiment-update'),
    url(r'^batiment/delete/(?P<pk>[0-9]+)/$', views.BatimentDelete.as_view(), name='batiment-delete'),
    url(r'^batiments/$', views.BatimentList.as_view(), name='batiment_list'),
    url(r'^batiment/deletep/([0-9]+)/$', proprietaire.delete_proprietaire_batiment, name='delete_proprietaire_batiment'),



    # url(r'^proprietaire/create/$', views.ProprietaireCreate.as_view(), name='proprietaire-create'),
    # url(r'^proprietaire/createb/(?P<pk>[0-9]+)/$', views.ProprietaireCreateForBatiment.as_view(), name='proprietaire-create-batiment'),
    # url(r'^proprietaire/update/(?P<pk>[0-9]+)/$', views.ProprietaireUpdate.as_view(), name='proprietaire-update'),
    # url(r'^proprietaire/delete/(?P<pk>[0-9]+)/$', views.ProprietaireDelete.as_view(), name='proprietaire-delete'),
    # url(r'^proprietaires/$', views.ProprietaireList.as_view(), name='proprietaire_list'),
    # url(r'^proprietaire/(?P<pk>[0-9]+)/$', views.ProprietaireDetail.as_view(), name='proprietaire_detail'),

    url(r'^contratgestion/create/([0-9]+)/$', contratgestion.create, name='contratgestion-create'),
    # url(r'^contratgestion/update/(?P<pk>[0-9]+)/$', views.ContratGestionUpdate.as_view(), name='contratgestion-update'),
    url(r'^contratgestion/delete/([0-9]+)/$', contratgestion.delete, name='contratgestion-delete'),
    url(r'^gestion/prepare/update/all/([0-9]+)/$', contratgestion.prepare_update, name='gestion-prepare-update-all'),
    url(r'^gestion/update/all/$', contratgestion.update, name='update-gestion-all'),



    url(r'^contratgestions/$', contratgestion.list, name='contratgestion_list'),

    # url(r'^contratgestion/(?P<pk>[0-9]+)/$', views.ContratGestionDetail.as_view(), name='contratgestion'),

    url(r'^societe/create/$', views.SocieteCreate.as_view(), name='societe-create'),
    url(r'^societe/update/(?P<pk>[0-9]+)/$', views.SocieteUpdate.as_view(), name='societe-update'),
    url(r'^societe/delete/(?P<pk>[0-9]+)/$', views.SocieteDelete.as_view(), name='societe-delete'),
    url(r'^societes/$', views.SocieteList.as_view(), name='societe_list'),
    url(r'^societe/(?P<pk>[0-9]+)/$', views.SocieteDetail.as_view(), name='societe'),
    # url(r'^batiment5/(?P<pk>\d+)/$', BatimentDetailView.as_view(), batiment_info)
    url(r'^alertes/$', alertes.list, name='alerte_list'),
    url(r'^alertes/update/([0-9]+)/$', alertes.update, name='alerte-update'),

    # url(r'^location/create/$', views.ContratLocationCreate.as_view(), name='location-create'),
    # url(r'^location/update/(?P<pk>[0-9]+)/$', views.ContratLocationUpdate.as_view(), name='location-update'),

    url(r'^location/prepare/update/all/([0-9]+)/$', contratlocation.prepare_update, name='location-prepare-update-all'),
    url(r'^location/update/all/$', contratlocation.update, name='update-location-all'),
    url(r'^location/createb/([0-9]+)/$', contratlocation.contrat_location_for_batiment, name='location-create-batiment'),
    url(r'^location/createl/$', contratlocation.test, name='add-location-for-batiment'),

    url(r'^location/delete/([0-9]+)/$', contratlocation.delete, name='location-delete'),
    # url(r'^location/(?P<pk>[0-9]+)/$', views.ContratLocationDetail.as_view(), name='contratlocation_detail'),
    # url(r'^contratlocations/$', views.ContratLocationList.as_view(), name='contratlocation_list'),
    url(r'^contratlocations/$', contratlocation.list, name='contratlocation_list'),
    url(r'^location/delete/$', contratlocation.confirm_delete, name='confirm-delete-location'),

    url(r'^financement/new/([0-9]+)/$', financement.new, name='financement-new'),
    url(r'^financement/create/$', financement.create, name='create-financement'),
    url(r'^locataire/new/([0-9]+)/$', locataire.new, name='locataire-new'),
    url(r'^locataire/add/$', locataire.add, name='locataire-add'),
    url(r'^locataire/delete/([0-9]+)/$', locataire.delete, name='locataire-delete'),
    url(r'^locataires/$', locataire.list, name='locataire-list'),
    url(r'^locataire/([0-9]+)/$', locataire.locataire_form, name='locataire'),
    url(r'^locataire/update/([0-9]+)/$', locataire.update, name='locataire-update'),

    url(r'^honoraires/$', honoraire.list, name='honoraire-list'),
    url(r'^honoraires/search/$', honoraire.search, name='honoraires-search'),
    url(r'^honoraire/update/$', honoraire.update, name='honoraire-update'),
    url(r'^honoraire/([0-9]+)/$', honoraire.honoraire_form, name='honoraire'),
    url(r'^honoraire/delete/(?P<pk>[0-9]+)/$', views.HonoraireDelete.as_view(), name='honoraire-delete'),
    url(r'^test/$', views.test, name='test'),
    url(r'^test/image/$', views.test_image, name='test_image'),
    url(r'^test/merge/$', views.test_merge, name='test_merge'),
    url(r'^test/upload/$', views.upload,name='upload'),
    url(r'^test/upload2/$', tests.test_create_pdf,name='test_pdf'),
    url(r'^test3/$', test3.test,name='test3'),

    url(r'^assurance_create/$', assurance.create, name='assurance_create'),

]
