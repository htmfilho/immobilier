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
import datetime
import factory
import factory.fuzzy
from main.tests.factories.personne import PersonneFactory
from main.tests.factories.batiment import BatimentFactory
from django.utils import timezone

def generate_date_fin(contrat):
    return datetime.date(contrat.date_debut.year,12,31)

class ContratGestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'main.ContratGestion'

    batiment = factory.SubFactory(BatimentFactory)
    gestionnaire = factory.SubFactory(PersonneFactory)
    date_debut = factory.fuzzy.FuzzyDate(datetime.date(timezone.now().year, 1, 1),datetime.date(timezone.now().year+10, 1, 1))
    date_fin = generate_date_fin
    montant_mensuel = factory.fuzzy.FuzzyDecimal(250.50, 480.0)
