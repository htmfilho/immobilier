from django.contrib import admin
from .models import Personne
from .models import Assurance
from .models import Banque
from .models import Batiment
from .models import FinancementLocation
from .models import Locataire
from .models import ContratLocation
from .models import ContratGestion
from .models import FraisMaintenance
from .models import SuiviLoyer
from .models import Proprietaire
from .models import ModeleDocument
from .models import Photo
from .models import Societe
from .models import Alerte
from .models import Pays
from .models import Localite
from .models import Honoraire

from .exportUtils import export_xls_batiment
from .pdfUtils import pdf_batiment

class PersonneAdmin(admin.ModelAdmin):
    search_fields = ['nom']
    list_filter = ('nom','prenom',)

admin.site.register(Personne,PersonneAdmin)
admin.site.register(Assurance)
admin.site.register(Banque)

class BatimentAdmin(admin.ModelAdmin):
    search_fields = ['localite']
    actions = [export_xls_batiment, pdf_batiment]

admin.site.register(Batiment,BatimentAdmin)

admin.site.register(FinancementLocation)
admin.site.register(Locataire)
admin.site.register(ContratLocation)
admin.site.register(ContratGestion)
admin.site.register(FraisMaintenance)
admin.site.register(SuiviLoyer)
admin.site.register(Proprietaire)
admin.site.register(ModeleDocument)
admin.site.register(Photo)
admin.site.register(Societe)
admin.site.register(Alerte)
admin.site.register(Pays)
admin.site.register(Localite)
admin.site.register(Honoraire)
