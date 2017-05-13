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
from main.models import personne, assurance, banque, batiment, financement_location, locataire, contrat_location\
    , contrat_gestion, frais_maintenance, suivi_loyer, professionnel, proprietaire, modele_document, photo, societe\
    , alerte, pays, localite, honoraire, fonction, type_societe, indice_sante


admin.site.register(personne.Personne, personne.PersonneAdmin)
admin.site.register(assurance.Assurance)
admin.site.register(banque.Banque)
admin.site.register(batiment.Batiment, batiment.BatimentAdmin)
admin.site.register(financement_location.FinancementLocation)
admin.site.register(locataire.Locataire)
admin.site.register(contrat_location.ContratLocation)
admin.site.register(contrat_gestion.ContratGestion)
admin.site.register(frais_maintenance.FraisMaintenance)
admin.site.register(suivi_loyer.SuiviLoyer, suivi_loyer.SuiviLoyerAdmin)
admin.site.register(proprietaire.Proprietaire)
admin.site.register(modele_document.ModeleDocument)
admin.site.register(photo.Photo)
admin.site.register(societe.Societe, societe.SocieteAdmin)
admin.site.register(alerte.Alerte, alerte.AlerteAdmin)
admin.site.register(pays.Pays)
admin.site.register(localite.Localite)
admin.site.register(honoraire.Honoraire, honoraire.HonoraireAdmin)
admin.site.register(fonction.Fonction)
admin.site.register(professionnel.Professionnel, professionnel.ProfessionnelAdmin)
admin.site.register(type_societe.TypeSociete)
admin.site.register(indice_sante.IndiceSante, indice_sante.IndiceSanteAdmin)
