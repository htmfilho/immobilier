from django import forms
from django.forms import ModelForm
from main.models import Personne, Batiment, Proprietaire, FraisMaintenance
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class PersonneForm(ModelForm):

    class Meta:
        model = Personne
        fields=['nom','prenom','societe','email','profession','date_naissance','lieu_naissance','pays_naissance','num_identite','telephone','gsm']

    def __init__(self, *args, **kwargs):
        print('personneForm 2')
        super(PersonneForm, self).__init__(*args, ** kwargs)
        print('personneForm 1')
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-offset-1 col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.add_input(Submit('submit','Ok'))

class BatimentForm(ModelForm):

    class Meta:
        model = Batiment
        fields=['description','rue','numero','boite','lieu_dit','code_postal','localite','superficie','peformance_energetique','photo']


    def __init__(self, *args, **kwargs):
        super(BatimentForm, self).__init__(*args, ** kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-offset-1 col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.add_input(Submit('submit','Ok'))


class ProprietaireForm(ModelForm):

    class Meta:
        model = Proprietaire
        fields=['proprietaire','batiment','date_debut','date_fin']


    def __init__(self, *args, **kwargs):
        super(ProprietaireForm, self).__init__(*args, ** kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-offset-1 col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.add_input(Submit('submit','Ok'))


class FraisMaintenanceForm(ModelForm):

    class Meta:
        model = FraisMaintenance
        fields=['proprietaire','entrepreneur','description','montant','date_realisation']


    def __init__(self, *args, **kwargs):
        super(FraisMaintenanceForm, self).__init__(*args, ** kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-offset-1 col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.add_input(Submit('submit','Ok'))
