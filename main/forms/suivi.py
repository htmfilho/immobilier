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
from main import models as mdl
from main.forms.utils.datefield import DatePickerInput, DATE_FORMAT
from main.models.enums import etat_suivi as etat_suivi_enum


READONLY_ATTR = "disabled"


class SuiviForm(forms.ModelForm):
    date_paiement = forms.HiddenInput()
    financement_location = forms.HiddenInput()
    date_paiement_reel = forms.DateField(widget=DatePickerInput(format=DATE_FORMAT),
                                         input_formats=[DATE_FORMAT, ],
                                         required=False)


    class Meta:
        model = mdl.suivi_loyer.SuiviLoyer
        fields = ['date_paiement', 'financement_location', 'etat_suivi', 'remarque', 'loyer_percu', 'charges_percu',
                  'date_paiement_reel']

    def __init__(self, *args, **kwargs):
        super(SuiviForm, self).__init__(*args, **kwargs)
        self.fields['date_paiement'].widget = forms.HiddenInput()
        self.fields['financement_location'].widget = forms.HiddenInput()

        self.fields['date_paiement_reel'].help_text = '(Double clic = date du jour)'
        if self.instance:
            self.fields['loyer_percu'].help_text = '(Montant attendu : {})'.format(self.instance.financement_location.loyer)
            self.fields['charges_percu'].help_text = '(Montant attendu : {})'.format(self.instance.financement_location.charges)


    def clean(self):
        self.validate_dates()
        self.validate_status()


    def validate_status(self):
        if self.cleaned_data.get("etat_suivi") == etat_suivi_enum.PAYE and \
                (self.cleaned_data.get("loyer_percu") is None or self.cleaned_data.get("loyer_percu") == 0) and \
                (self.cleaned_data.get("charges_percu") is None or self.cleaned_data.get("charges_percu") == 0):
            msg = u"L'état ne peut pas être à 'PAYE' si aucun montant n'est introduit pour les loyer/charge percue(s)"
            self._errors["etat_suivi"] = self.error_class([msg])

    def validate_dates(self):
        date_paiement = self.cleaned_data.get("date_paiement")
        date_paiement_reel = self.cleaned_data.get("date_paiement_reel")
        if date_paiement_reel and date_paiement and date_paiement_reel < date_paiement:
            msg = u"La date réelle de paiement doit être supérieure ou égale à la date supposée du paiement"
            self._errors["date_paiement_reel"] = self.error_class([msg])

