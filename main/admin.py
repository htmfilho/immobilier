from django.contrib import admin
from .models import Personne
from .models import Assurance
from .models import Banque
from .models import Batiment
from .models import Location
from .models import Locataire

admin.site.register(Personne)
admin.site.register(Assurance)
admin.site.register(Banque)
admin.site.register(Batiment)
admin.site.register(Location)
admin.site.register(Locataire)
