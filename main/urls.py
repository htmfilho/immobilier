from django.conf.urls import url
from django.conf import settings
from . import views, batiment, proprietaire, suivis
from .models import Batiment, Proprietaire, ContratGestion
from main.views import BatimentDetailView
from django.conf.urls import url
from django.contrib.auth.views import login,logout
from django.views.generic import ListView
from main.views import ContratGestionList


# batiment_info = {
#     'queryset': Batiment.objects.get(nom='batiment 5b')    ,
#     'template_name': 'batiment_detail.html',
#     'template_object_name': 'batiment',
#     'extra_context': {'proprietaire_list': Proprietaire.objects.all()}
# }
urlpatterns = [
    url(r'^$', views.home, name='home'),
    # login / logout urls
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    # listes
    url(r'^listeComplete', views.listeComplete),
    url(r'^listeBatiments', views.listeBatiments, name='listeBatiments'),
    # url(r'^listeProprietaires', views.listeProprietaires, name='listeProprietaires'),
    url(r'^listeContratGestion/$', views.ContratGestionList.as_view(), name='contrat_gestion_list'),
    url(r'^contratGestion/(?P<pk>[0-9]+)/$', views.ContratGestionDetail.as_view(), name='contrat_gestion_detail'),
    # ecran de detail
    url(r'^batiment/([0-9]+)/$', batiment.batiment, name='batiment'),
    # url(r'^proprietaire/([0-9]+)/$', proprietaire.proprietaire, name='proprietaire'),
    # url(r'^proprietaire/update/([0-9]+)/$', proprietaire.update_proprietaire, name='update_proprietaire'),
    # url(r'^proprietaire/delete/([0-9]+)/$', proprietaire.delete_proprietaire, name='delete_proprietaire'),
    # url(r'^proprietaire/dadd/([0-9]+)/$', proprietaire.add_proprietaire, name='add_proprietaire'),
    #old
    # url(r'^suivis/$', suivis.suivis, name='suivis'),
    # url(r'^suivis/refresh/$', suivis.refresh_suivis, name='refresh_suivis'),
    url(r'^suivis/$', suivis.suivis, name='suivis'),
    url(r'^suivis/search$', suivis.suivis_search, name='suivis_search'),

    # url(r'^update_personne/$', views.update_personne, name='update_personne'),
    url(r'^update_batiment/$', batiment.update, name='update_batiment'),

    # test
    url(r'^xlsRead', views.xlsRead, name='xlsRead'),

    url(r'^photos/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    url(r'^test4', views.alertes4),

    url(r'^fraismaintenances/$', views.FraisMaintenanceList.as_view(), name='fraismaintenance_list'),
    url(r'^fraismaintenance/create/$', views.FraisMaintenanceCreate.as_view(), name='fraismaintenance-create'),
    url(r'^fraismaintenance/update/(?P<pk>[0-9]+)/$', views.FraisMaintenanceUpdate.as_view(), name='fraismaintenance-update'),
    url(r'^fraismaintenance/delete/(?P<pk>[0-9]+)/$', views.FraisMaintenanceDelete.as_view(), name='fraismaintenance-delete'),
    url(r'^fraismaintenance/(?P<pk>[0-9]+)/$', views.FraisMaintenanceDetail.as_view(), name='fraismaintenance_detail'),


    url(r'^personne/create/$', views.PersonneCreate.as_view(), name='personne-create'),
    url(r'^personne/update/(?P<pk>[0-9]+)/$', views.PersonneUpdate.as_view(), name='personne-update'),
    url(r'^personne/delete/(?P<pk>[0-9]+)/$', views.PersonneDelete.as_view(), name='personne-delete'),
    url(r'^personnes/$', views.PersonneList.as_view(), name='personne_list'),
    url(r'^personne/(?P<pk>[0-9]+)/$', views.PersonneDetail.as_view(), name='personne_detail'),

    url(r'^batiment/create/$', views.BatimentCreate.as_view(), name='batiment-create'),
    url(r'^batiment/update/(?P<pk>[0-9]+)/$', views.BatimentUpdate.as_view(), name='batiment-update'),
    url(r'^batiment/delete/(?P<pk>[0-9]+)/$', views.BatimentDelete.as_view(), name='batiment-delete'),
    url(r'^batiments/$', views.BatimentList.as_view(), name='batiment_list'),

    url(r'^proprietaire/create/$', views.ProprietaireCreate.as_view(), name='proprietaire-create'),
    url(r'^proprietaire/update/(?P<pk>[0-9]+)/$', views.ProprietaireUpdate.as_view(), name='proprietaire-update'),
    url(r'^proprietaire/delete/(?P<pk>[0-9]+)/$', views.ProprietaireDelete.as_view(), name='proprietaire-delete'),
    url(r'^proprietaires/$', views.ProprietaireList.as_view(), name='proprietaire_list'),
    url(r'^proprietaire/(?P<pk>[0-9]+)/$', views.ProprietaireDetail.as_view(), name='proprietaire_detail'),

    # url(r'^batiment5/(?P<pk>\d+)/$', BatimentDetailView.as_view(), batiment_info)
]
