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

class ContratGestionForm(forms.ModelForm):
    date_debut = forms.DateField(widget=DatePickerInput(format=DATE_FORMAT),
                                 input_formats=[DATE_FORMAT, ],
                                 required=False)
    date_fin = forms.DateField(widget=DatePickerInput(format=DATE_FORMAT),
                               input_formats=[DATE_FORMAT, ],
                               required=False)
    # batiment = forms.ModelChoiceField(
    #     queryset=mdl.batiment.Batiment.objects.all(),
    #     widget=forms.MultipleHiddenInput())
    #
    # gestionnaire = forms.ModelChoiceField(
    #     queryset=mdl.personne.find_gestionnaire_default(),
    #     widget=forms.MultipleHiddenInput())

    class Meta:
        model = mdl.contrat_gestion.ContratGestion
        fields = ['id', 'batiment', 'gestionnaire', 'date_debut', 'date_fin', 'montant_mensuel']


    def __init__(self, *args, **kwargs):

        # self.batiment = kwargs.pop('batiment', None)
        super(ContratGestionForm, self).__init__(*args, ** kwargs)
        # if self.batiment:
        #     print('if {}'.format(self.batiment.id))
        # else:
        #     print('elses')

        # instance = getattr(self, 'instance', None)
        # self.fields['gestionnaire'].widget.attrs[READONLY_ATTR] = READONLY_ATTR
        # if instance.batiment and instance.batiment.pk:
        #     print('init if')
            # self.fields['batiment'].widget.attrs[READONLY_ATTR] = READONLY_ATTR
        # else:
        #     print('init else')
        # if self.instance:
            # self.fields['batiment_name'] = forms.CharField(max_length=200, required=False, disabled=True,
            #                                                label='Batiment concerné')
            # if self.instance.batiment:
            #     self.fields['batiment_name'].initial = self.instance.batiment
            #     self.fields['batiment_name'].initial = '-'
        # self.fields['batiment'].widget.attrs[READONLY_ATTR] = READONLY_ATTR

        # self.fields['batiment'].widget = forms.HiddenInput()
        # self.fields['gestionnaire'].widget = forms.HiddenInput()

        self.fields["date_debut"].required = True
        self.fields["date_fin"].required = True
        self.fields["montant_mensuel"].required = True
        # self.fields['batiment'].widget.attrs['disabled'] = 'disabled'
        # self.fields['gestionnaire'].widget.attrs['disabled'] = 'disabled'

    # def clean_date_debut(self):
    #     date_debut = self.cleaned_data['date_debut']
    #     date_fin = self.cleaned_data['date_fin']
    #     if date_debut and date_fin:
    #         if date_debut >= date_fin:
    #             raise ValidationError('Dates erronées la date de début doit être inférieure à la date de fin')
    #
    #     return date_debut
    #
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('date_debut') and cleaned_data.get('date_fin'):
            if cleaned_data.get('date_debut') > cleaned_data.get('date_fin'):
                msg = u"Dates erronées la date de début doit être inférieure à la date de fin"
                self._errors["date_debut"] = self.error_class([msg])

        return cleaned_data


    def save(self, commit=True):
        print('save')

        instance=super(ContratGestionForm, self).save(commit=False)
        if commit:
            instance.save()
            return instance
        print(instance.id)

    def save(self, commit=True):
        instance = super(ContratGestionForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance

    # avant ce qu'il y a ci-dessous
    #
    # batiment_id = forms.ModelChoiceField(queryset=mdl.batiment.find_all())
    #
    # date_debut = forms.DateField(required=True, input_formats=[views_utils.DATE_SHORT_FORMAT],
    #                              widget=forms.DateInput(format=views_utils.DATE_SHORT_FORMAT))
    # date_fin = forms.DateField(required=False, input_formats=[views_utils.DATE_SHORT_FORMAT],
    #                            widget=forms.DateInput(format=views_utils.DATE_SHORT_FORMAT))
    # montant_mensuel = forms.DecimalField(max_digits=6, decimal_places=2, localize=True)
    #
    # class Meta:
    #     model = contrat_gestion.ContratGestion
    #     fields = ['montant_mensuel']
    #
    # def __init__(self, *args, **kwargs):
    #     super(ContratGestionForm, self).__init__(*args, ** kwargs)
    #
    # def clean(self):
    #     cleaned_data = super(ContratGestionForm, self).clean()
    #     if cleaned_data.get('date_debut') and cleaned_data.get('date_fin'):
    #         if cleaned_data.get('date_debut') > cleaned_data.get('date_fin'):
    #             self.errors['date_debut'] = 'Dates erronées'
    #     return cleaned_data
