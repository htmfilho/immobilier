##############################################################################
#
#    Immobilier it's an application
#    designed to manage the core business of property management, buildings,
#    rental agreement and so on.
#
#    Copyright (C) 2016-2017 Verpoorten Leïla
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
from .models import Fonction
from .models import Professionnel
from .models import TypeSociete
from .exportUtils import export_xls_batiment
from .pdfUtils import pdf_batiment


class PersonneAdmin(admin.ModelAdmin):
    search_fields = ['nom']
    list_filter = ('nom','prenom',)

admin.site.register(Personne, PersonneAdmin)
admin.site.register(Assurance)
admin.site.register(Banque)


class BatimentAdmin(admin.ModelAdmin):
    search_fields = ['localite']
    actions = [export_xls_batiment, pdf_batiment]

admin.site.register(Batiment, BatimentAdmin)

admin.site.register(FinancementLocation)
admin.site.register(Locataire)
admin.site.register(ContratLocation)
admin.site.register(ContratGestion)
admin.site.register(FraisMaintenance)
admin.site.register(SuiviLoyer)
admin.site.register(Proprietaire)
admin.site.register(ModeleDocument)
admin.site.register(Photo)


class SocieteAdmin(admin.ModelAdmin):
    search_fields = ['nom']
    list_filter = ('localite',)

admin.site.register(Societe, SocieteAdmin)


class AlertAdmin(admin.ModelAdmin):
    list_filter = ('etat',)

admin.site.register(Alerte, AlertAdmin)
admin.site.register(Pays)
admin.site.register(Localite)


class HonoraireAdmin(admin.ModelAdmin):
    list_filter = ('etat',)

admin.site.register(Honoraire, HonoraireAdmin)
admin.site.register(Fonction)
admin.site.register(Professionnel)
admin.site.register(TypeSociete)
