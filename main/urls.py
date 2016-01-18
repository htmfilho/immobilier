from django.conf.urls import url
from django.conf import settings
from . import views
from .models import Batiment, Proprietaire
from main.views import BatimentDetailView
from django.conf.urls import url
from django.contrib.auth.views import login,logout

batiment_info = {
    'queryset': Batiment.objects.get(nom='batiment 5b')    ,
    'template_name': 'batiment_detail.html',
    'template_object_name': 'batiment',
    'extra_context': {'proprietaire_list': Proprietaire.objects.all()}
}
urlpatterns = [
    url(r'^$', views.home, name='home'),
    # login / logout urls
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    # listes
    url(r'^listeComplete', views.listeComplete),    
    url(r'^listeBatiments', views.listeBatiments, name='listeBatiments'),    
    url(r'^listeProprietaires', views.listeProprietaires, name='listeProprietaires'),    
    url(r'^listePersonnes', views.listePersonnes, name='listePersonnes'),    
    # ecran de detail
    url(r'^batiment/([0-9]+)/$', views.batiment, name='batiment'),    
    url(r'^proprietaire/([0-9]+)/$', views.proprietaire, name='proprietaire'),    
    url(r'^personne/([0-9]+)/$', views.personne, name='personne'),    
    # test
    url(r'^xlsRead', views.xlsRead, name='xlsRead'),    
    
    url(r'^photos/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    url(r'^test4', views.alertes4),
    url(r'^batiment5/(?P<pk>\d+)/$', BatimentDetailView.as_view(), batiment_info)
]
