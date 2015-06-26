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

admin.site.register(Personne)
admin.site.register(Assurance)
admin.site.register(Banque)
admin.site.register(Batiment)
admin.site.register(FinancementLocation)
admin.site.register(Locataire)
admin.site.register(ContratLocation)
admin.site.register(ContratGestion)
admin.site.register(FraisMaintenance)
admin.site.register(SuiviLoyer)
admin.site.register(Proprietaire)
admin.site.register(ModeleDocument)
admin.site.register(Photo)

