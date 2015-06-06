from django.contrib import admin
from .models import Personne
from .models import Assurance
from .models import Banque

admin.site.register(Personne)
admin.site.register(Assurance)
admin.site.register(Banque)