from django import forms
from django.forms import ModelForm
from main.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from main import views_utils

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


class PersonneForm(forms.Form):
    # fonctionnepays_naissance = forms.ChoiceField(choices=get_pays_choix())
    class Meta:
        model = Personne
        fields = ['nom', 'prenom', 'email', 'profession', 'date_naissance', 'lieu_naissance', 'pays_naissance',
                  'num_identite', 'telephone', 'gsm', 'societe']
        autocomplete_fields = ('prenom', 'profession', 'lieu_naissance', 'pays_naissance')

    def num_identite(self):
        if self.cleaned_data['num_identite'] == "":
            return None
        else:
            return self.cleaned_data['num_identite']

    def __init__(self, *args, **kwargs):
        super(PersonneForm, self).__init__(*args, ** kwargs)


class BatimentForm(forms.Form):
    superficie = forms.DecimalField(required=False, max_digits=8, decimal_places=3, localize=True)

    def __init__(self, *args, **kwargs):
        super(BatimentForm, self).__init__(*args, ** kwargs)

    def clean(self):
        cleaned_data = super(BatimentForm, self).clean()
        if cleaned_data.get('superficie') and cleaned_data.get('superficie') < 0:
            self.errors['superficie'] = 'Si une superficie est encodée elle doit être > à 0'


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


class FraisMaintenanceForm(forms.Form):
    date_realisation = forms.DateField(required=False, input_formats=[views_utils.DATE_SHORT_FORMAT],
                                       widget=forms.DateInput(format=views_utils.DATE_SHORT_FORMAT))
    montant = forms.DecimalField(required=True, max_digits=8, decimal_places=2, localize=True)

    def __init__(self, *args, **kwargs):
        super(FraisMaintenanceForm, self).__init__(*args, ** kwargs)


class SocieteForm(ModelForm):

    class Meta:
        model = Societe
        fields = ['nom', 'description', 'rue', 'numero', 'boite', 'lieu_dit', 'code_postal', 'localite']

    def __init__(self, *args, **kwargs):
        super(SocieteForm, self).__init__(*args, ** kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-offset-1 col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.add_input(Submit('submit', 'Ok'))


class ContratLocationForm(forms.Form):

    date_debut = forms.DateField(required=True, input_formats=[views_utils.DATE_SHORT_FORMAT],
                                 widget=forms.DateInput(format=views_utils.DATE_SHORT_FORMAT))
    # date_fin = forms.DateField(required=False, input_formats=['%d/%m/%Y'],
    #                            widget=forms.DateInput(format='%d/%m/%Y'))
    # renonciation = forms.DateField(required=False, input_formats=['%d/%m/%Y'],
    #                                widget=forms.DateInput(format='%d/%m/%Y'))
    loyer_base = forms.DecimalField(required=True, max_digits=8, decimal_places=2, localize=True)
    charges_base = forms.DecimalField(required=True, max_digits=8, decimal_places=2, localize=True)
    assurance = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(ContratLocationForm, self).__init__(*args, ** kwargs)

    def clean(self):
        cleaned_data = super(ContratLocationForm, self).clean()
        if cleaned_data.get('date_debut') and cleaned_data.get('date_fin'):
            if cleaned_data.get('date_debut') > cleaned_data.get('date_fin'):
                self.errors['date_debut'] = 'Dates erronées'
        if cleaned_data.get('loyer_base') <= 0 and cleaned_data.get('charges_base') <= 0:
            self.errors['loyer_base'] = 'Il faut au minimun un loyer ou des charges'
        return cleaned_data

    def clean_assurance(self):
        data = self.cleaned_data['assurance']

        if data is None or data == '-':
            data = None
        return data

    def clean_date_debut(self):
        data = self.cleaned_data['date_debut']

        if data is None or data == '-':
            data = None
        return data


class HonoraireForm(ModelForm):

    class Meta:
        model = Honoraire
        fields = ['date_paiement', 'etat']

    def __init__(self, *args, **kwargs):
        super(HonoraireForm, self).__init__(*args, ** kwargs)


class FinancementLocationForm(forms.Form):
    date_debut = forms.DateField(required=True, input_formats=[views_utils.DATE_SHORT_FORMAT],
                                 widget=forms.DateInput(format=views_utils.DATE_SHORT_FORMAT))
    date_fin = forms.DateField(required=False, input_formats=[views_utils.DATE_SHORT_FORMAT],
                               widget=forms.DateInput(format=views_utils.DATE_SHORT_FORMAT))
    loyer = forms.DecimalField(required=True, max_digits=8, decimal_places=2, localize=True)
    charges = forms.DecimalField(required=True, max_digits=8, decimal_places=2, localize=True)
    index = forms.DecimalField(required=True, max_digits=8, decimal_places=2, localize=True)

    class Meta:
        model = FinancementLocation
        fields = ['date_debut', 'date_fin', 'loyer', 'charges', 'index']


class FileForm(forms.Form):
    file = forms.FileField()


class ContratGestionForm(forms.Form):
    batiment_id = forms.ChoiceField(widget=forms.Select(attrs={'class': 'selector'}))
    # batiments=[]
    # for x in Batiment.objects.all():
    #     batiments.append(x.id)

    # batiments =  [(x.id) for x in Batiment.objects.all()]
    # print(batiments)
    # batiment_id = forms.ModelChoiceField(queryset=Batiment.objects.all())
    date_debut = forms.DateField(required=True, input_formats=[views_utils.DATE_SHORT_FORMAT],
                                 widget=forms.DateInput(format=views_utils.DATE_SHORT_FORMAT))
    date_fin = forms.DateField(required=False, input_formats=[views_utils.DATE_SHORT_FORMAT],
                               widget=forms.DateInput(format=views_utils.DATE_SHORT_FORMAT))
    montant_mensuel = forms.DecimalField(max_digits=6, decimal_places=2, localize=True)

    class Meta:
        model = ContratGestion
        fields = ['montant_mensuel']

    def __init__(self, *args, **kwargs):
        super(ContratGestionForm, self).__init__(*args, ** kwargs)
        self.fields["batiment_id"].queryset = Batiment.find_all()

    def clean(self):
        cleaned_data = super(ContratGestionForm, self).clean()
        if cleaned_data.get('date_debut') and cleaned_data.get('date_fin'):
            if cleaned_data.get('date_debut') > cleaned_data.get('date_fin'):
                self.errors['date_debut'] = 'Dates erronées'
        if cleaned_data.get('batiment_id'):
            print(cleaned_data.get('batiment_id'))
            print('if')
        else:
            print('else')
            print(cleaned_data.get('batiment_id'))
        return cleaned_data


class SuiviForm(forms.Form):
    date_paiement_reel = forms.DateField(required=False, input_formats=[views_utils.DATE_SHORT_FORMAT],
                                         widget=forms.DateInput(format=views_utils.DATE_SHORT_FORMAT))

    def __init__(self, *args, **kwargs):
        super(SuiviForm, self).__init__(*args, ** kwargs)
