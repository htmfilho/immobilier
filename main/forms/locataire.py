##############################################################################
#
#    Immobilier it's an application
#    designed to manage the core business of property management, buildings,
#    rental agreement and so on.
#
#    Copyright (C) 2016-2018 Verpoorten Leïla
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
from django import forms
from main.models.locataire import Locataire


class LocataireForm(forms.ModelForm):

    class Meta:
        model = Locataire
        fields = ['personne', 'civilite', 'infos_complement', 'societe', 'profession', 'tva', 'principal', 'actif',
                  'contrat_location']


    def __init__(self, data=None, initial=None, *args, **kwargs):
        super().__init__(data, initial=initial, **kwargs)
        self.fields['societe'].label = 'Societé occupant les lieux'
        self.fields['profession'].label = 'Fonction exercée dans les lieux'
        self.fields['profession'].label = 'Fonction exercée dans les lieux'
        self.fields['contrat_location'].widget=forms.HiddenInput()

