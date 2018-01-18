from django.conf.urls import include, url
from django.contrib import admin
from main import assurance
urlpatterns = [
    url(r'', include('main.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^assurance_create/$', assurance.create, name='assurance_create'),
]
