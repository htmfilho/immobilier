from django.contrib import admin
from .models import Personne
from .models import Assurance
from .models import Banque
from .models import Batiment
from .models import Location
from .models import Locataire
from .models import Contrat
from .models import ContratGestion
from .models import FraisMaintenance
from .models import SuiviLoyer
from .models import Proprietaire

admin.site.register(Personne)
admin.site.register(Assurance)
admin.site.register(Banque)
admin.site.register(Batiment)
admin.site.register(Location)
admin.site.register(Locataire)
admin.site.register(Contrat)
admin.site.register(ContratGestion)
admin.site.register(FraisMaintenance)
admin.site.register(SuiviLoyer)
admin.site.register(Proprietaire)
