from django import forms
from django.forms import ModelForm
from main.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.shortcuts import render, get_object_or_404


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


def get_pays_choix():
    choices_tuple = []

    list_pays = Pays.objects.all()
    # list_pays = Personne.objects.values('pays_naissance').distinct()
    # list_pays = Personne.objects.all().distinct('pays_naissance')
    # list_pays = Personne.objects.order_by('pays_naissance').values_list('pays_naissance', flat=True).distinct())
    # print (list(set(Personne.objects.values_list('pays_naissance', flat=True))))
    # print (list_pays)
    for p in list_pays:
        # print ('for')
        # print(p.pays)
        choices_tuple.append((p.pays, p.pays))
    if not choices_tuple:
        choices_tuple.append(('Belgique', 'Belgique'))

    # print(choices_tuple)
    return choices_tuple


class PersonneForm(ModelForm):
    # fonctionnepays_naissance = forms.ChoiceField(choices=get_pays_choix())
    class Meta:
        model = Personne
        fields = ['nom', 'prenom', 'email', 'profession', 'date_naissance', 'lieu_naissance', 'pays_naissance',
                  'num_identite', 'telephone', 'gsm']
        autocomplete_fields = ('prenom', 'profession', 'lieu_naissance', 'pays_naissance')

    def num_identite(self):
        if self.cleaned_data['num_identite'] == "":
            return None
        else:
            return self.cleaned_data['num_identite']

    def __init__(self, *args, **kwargs):

        super(PersonneForm, self).__init__(*args, ** kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-offset-1 col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.add_input(Submit('submit','Ok'))


class BatimentForm(ModelForm):

    class Meta:
        model = Batiment
        fields = ['description', 'rue', 'numero', 'boite', 'lieu_dit', 'localite', 'superficie',
                  'performance_energetique']

    def __init__(self, *args, **kwargs):
        super(BatimentForm, self).__init__(*args, ** kwargs)


class ProprietaireForm(forms.ModelForm):
    class Meta:
        model = Proprietaire
        fields = ['proprietaire', 'batiment', 'date_debut', 'date_fin']

    def __init__(self, *args, **kwargs):

        # # batiment = kwargs.pop('batiment')
        # batiment= kwargs.get('sheet_id', None)
        #
        # print(batiment)
        super(ProprietaireForm, self).__init__(*args, ** kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-offset-1 col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.add_input(Submit('submit', 'Ok'))


class FraisMaintenanceForm(ModelForm):

    class Meta:
        model = FraisMaintenance
        fields = ['batiment', 'entrepreneur', 'description', 'montant', 'date_realisation']


class SocieteForm(ModelForm):

    class Meta:
        model = Societe
        fields = ['nom', 'description', 'rue', 'numero', 'boite', 'lieu_dit', 'code_postal', 'localite', 'personnel']

    def __init__(self, *args, **kwargs):
        super(SocieteForm, self).__init__(*args, ** kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-offset-1 col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.add_input(Submit('submit','Ok'))


class ContratLocationForm(ModelForm):
    date_debut = forms.DateField(required=True, input_formats=['%d/%m/%Y'],
                                 widget=forms.DateInput(format='%d/%m/%Y'))
    date_fin = forms.DateField(required=True, input_formats=['%d/%m/%Y'],
                               widget=forms.DateInput(format='%d/%m/%Y'))
    loyer_base = forms.DecimalField(max_digits=8, decimal_places=2, localize=True)
    charges_base = forms.DecimalField(max_digits=8, decimal_places=2, localize=True)
    assurance = forms.CharField()

    class Meta:
        model = ContratLocation
        fields = ['date_debut', 'date_fin', 'renonciation', 'remarque', 'assurance', 'loyer_base', 'charges_base']

    def __init__(self, *args, **kwargs):
        super(ContratLocationForm, self).__init__(*args, ** kwargs)

    def clean(self):
        cleaned_data = super(ContratLocationForm, self).clean()
        if cleaned_data.get('date_debut') and cleaned_data.get('date_fin'):
            if cleaned_data.get('date_debut') > cleaned_data.get('date_fin'):
                self.errors['date_debut'] = 'Dates erronées'

        return cleaned_data

    def clean_assurance(self):
        data = self.cleaned_data['assurance']

        if data is None or data == '-':
            date = None
        return date
    #
    # def clean_loyer_base(self):
    #     data = self.cleaned_data['loyer_base']
    #     if data.


class HonoraireForm(ModelForm):

    class Meta:
        model = Honoraire
        fields=['date_paiement', 'etat']

    def __init__(self, *args, **kwargs):
        super(HonoraireForm, self).__init__(*args, ** kwargs)

# class FinancementLocationForm(forms.ModelForm):
#
#     date_debut = forms.DateField(('%d/%m/%Y',), label='Birth Date', required=False,
#         widget=forms.DateTimeInput(format='%d/%m/%Y', attrs={
#             'class':'input',
#             'size':'15'
#         })
#     )
#
#     class Meta:
#         model = FinancementLocation
#         fields=['date_debut','date_fin','loyer','charges','index']


class FileForm(forms.Form):
    file = forms.FileField()


class ContratGestionForm(ModelForm):
    montant_mensuel = forms.DecimalField(max_digits=6, decimal_places=2, localize=True)

    class Meta:
        model = ContratGestion
        fields = ['montant_mensuel']

    def __init__(self, *args, **kwargs):
        super(ContratGestionForm, self).__init__(*args, ** kwargs)

    def clean(self):
        cleaned_data = super(ContratGestionForm, self).clean()
        if cleaned_data.get('date_debut') and cleaned_data.get('date_fin'):
            if cleaned_data.get('date_debut') > cleaned_data.get('date_fin'):
                self.errors['date_debut'] = 'Dates erronées'

        return cleaned_data
