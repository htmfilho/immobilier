from django.db import models
from django import forms
from django.utils import timezone
import datetime

from dateutil.relativedelta import relativedelta
from django.core.urlresolvers import reverse
from django.core.exceptions import *

class Assurance(models.Model):
    nom         = models.CharField(max_length = 100)
    description = models.TextField(blank = True, null = True)

    def __str__(self):
        return self.nom
    class Meta:
        ordering = ['nom']


class Banque(models.Model):
    nom         = models.CharField(max_length = 100)
    description = models.TextField(blank = True, null = True)

    def __str__(self):
        return self.nom


class Photo(models.Model):
    photo     = models.FileField( upload_to="photos")
    texte     = models.TextField(default="")

    def __str__(self):
        return self.texte

def get_pays_choix():
    choices_tuple = []
    choices_tuple.append('Belgique')
    return choices_tuple


class Personne(models.Model):
    nom            = models.CharField(max_length = 100)
    prenom         = models.CharField(max_length = 100)
    # societe        = models.CharField(max_length = 100, blank = True, null = True)
    email          = models.EmailField(blank = True, null = True)
    profession     = models.CharField(max_length = 100, blank = True, null = True)
    date_naissance = models.DateField(auto_now = False, blank = True, null = True, auto_now_add = False)
    lieu_naissance = models.CharField(max_length = 100, blank = True, null = True)
    pays_naissance = models.CharField(max_length = 100, blank = True, null = True)
    num_identite   = models.CharField(max_length = 100, blank = True, null = True, unique=True)
    telephone      = models.CharField(max_length = 30, blank = True, null = True)
    gsm            = models.CharField(max_length = 30, blank = True, null = True)

    def __init__(self,  *args, **kwargs):
        super(Personne, self).__init__(*args, **kwargs)
        # self._meta.get_field_by_name('pays_naissance')[0]._choices = get_pays_choix()

    def __str__(self):
        return self.nom.upper() + ", " + self.prenom

    def choix(self):
        return []

    def find_personne(id):
        return Personne.objects.get(pk=id)

    @property
    def batiments(self):
        proprietaire_list =  Proprietaire.objects.filter(proprietaire=self)
        batiments=[]
        for p in proprietaire_list:
            # batiments.append(p.batiments)
            for b in p.batiments:
                batiments.append(b)
        return batiments

    def contrat_gestions(self):
        proprietaire_list =  Proprietaire.objects.filter(proprietaire=self)
        contrats=[]
        for p in proprietaire_list:

            for b in p.batiments:
                contrat_gestion = ContratGestion.objects.filter(batiment=b)
                if not contrat_gestion is None:
                    contrats.append(contrat_gestion)
        return contrats

    def find_all():
        return Personne.objects.all()

    def find_gestionnaire_default():
        nom='Marchal'
        prenom='Stéphan'
        list_personne =  Personne.objects.filter(nom=nom, prenom=prenom)
        if list_personne:
            return list_personne[0]
        return None


    class Meta:
        ordering = ['nom','prenom']
        unique_together = (("nom", "prenom"),)
    #
    # def get_absolute_url(self):
    #     return reverse('personne_list')

    def save(self,  *args, **kwargs):

        p=super(Personne, self).save(*args, **kwargs)
        if Pays.objects.filter(pays=self.pays_naissance):
            pass
        else:
            if not self.pays_naissance is None:
                pays = Pays(pays=self.pays_naissance)
                pays.save()
        return p

class Batiment(models.Model):
    description            = models.TextField(blank = True, null = True)
    rue                    = models.CharField(max_length = 200, blank = True, null = True)
    numero                 = models.IntegerField(blank = True, null = True)
    boite                  = models.CharField(max_length = 10, blank = True, null = True)
    lieu_dit               = models.CharField(max_length = 200, blank = True, null = True)
    code_postal            = models.CharField(max_length = 10, blank = True, null = True)
    localite               = models.CharField(max_length = 150, blank = True, null = True)
    # province               = models.CharField(max_length = 100, blank = True, null = True)
    superficie             = models.DecimalField(max_digits = 5, decimal_places = 3, blank = True, null = True)
    peformance_energetique = models.CharField(max_length = 10,blank = True, null = True)
    # photo                  = models.ManyToManyField(Photo, blank = True, null = True)

    class Meta:
        ordering = ['localite','rue']

    # def get_absolute_url(self):
        # return reverse('batiment_list')
        # return reverse('listeBatiments')


    def find_batiment(id):
        return Batiment.objects.get(pk=id)

    def __str__(self):
        desc = ""
        cptr=0
        if not(self.rue is None):
            desc += " " + self.rue
            cptr=cptr+1
        if not(self.numero is None):
            if cptr>0:
                desc += ", "
            desc += str(self.numero)
            cptr=cptr+1
        if not(self.boite is None):
            if cptr>0:
                desc += ", "
            desc += self.boite
            cptr=cptr+1
        if not(self.localite is None):
            if cptr>0:
                desc += ", "
            desc += self.localite
        return desc

    def adresse_rue(self):
        adresse_complete=""
        if self.rue is not None :
            adresse_complete += self.rue
        if self.numero is not None :
            adresse_complete += " " +str(self.numero)
        if self.boite is not None :
            adresse_complete += " " +str(self.boite)
        return adresse_complete

    def adresse_localite(self):
        adresse_complete=""
        if self.code_postal is not None :
            adresse_complete+= self.code_postal
        if self.localite is not None :
            adresse_complete+= " " + self.localite
        return adresse_complete

    def proprietaires(self):
        return Proprietaire.objects.filter(batiment=self)

    def contrats_location(self):
        return ContratLocation.objects.filter(batiment=self)

    def contrats_location_next(self):
        return ContratLocation.objects.filter(batiment=self, date_debut__gte=self.location_actuelle.date_fin)

    def contrats_location_previous(self):
        return ContratLocation.objects.filter(batiment=self, date_fin__lte=self.location_actuelle.date_debut)
    def contrat_location_next(self):
        list_c =  ContratLocation.objects.filter(batiment=self, date_debut__gte=self.location_actuelle.date_fin)
        if list_c:
            return list_c[0]
        return None


    def contrat_location_previous(self):
        list_c= ContratLocation.objects.filter(batiment=self, date_fin__lte=self.location_actuelle.date_debut)
        if list_c:
            return list_c[0]
        return None
        
    def locataires_actuels(self):
        liste=[]
        contrats = ContratLocation.objects.filter(batiment=self,date_debut__lte=timezone.now(), date_fin__gte=timezone.now() )
        if not(contrats is None):
            for contrat in contrats:
                locataire = Locataire.objects.filter(contrat_location=contrat)
                for l in locataire :
                    p = Personne.find_personne(l.personne.id)
                    liste.append(p)

        return liste
    @property
    def location_actuelle(self):
        return ContratLocation.objects.filter(batiment=self,date_debut__lte=timezone.now(), date_fin__gte=timezone.now() ).first()

    def location_actuelle_pk(self):
        contrat_location =  ContratLocation.objects.filter(batiment=self,date_debut__lte=timezone.now(), date_fin__gte=timezone.now() ).first()
        if contrat_location:
            return contrat_location.id
        return None

    @property
    def contrats_gestion(self):
        return ContratGestion.objects.filter(batiment=self)

    @property
    def frais_list(self):
        frais_list=[]
        for p in self.proprietaires:
            frais = FraisMaintenance.objects.filter(proprietaire=p)
            if not frais in frais_list:
                frais_list.append(frais)
        return frais_list


class Proprietaire(models.Model):
    proprietaire  = models.ForeignKey(Personne, verbose_name=u"Propriétaire")
    batiment      = models.ForeignKey(Batiment)
    date_debut    = models.DateField(auto_now = False, blank = True, null = True, auto_now_add = False, verbose_name=u"Date début")
    date_fin      = models.DateField(auto_now = False, blank = True, null = True, auto_now_add = False)

    def find_proprietaire(id):
        return Proprietaire.objects.get(pk=id)
    @property
    def batiments(self):
        return Batiment.objects.filter(proprietaire=self)

    def __str__(self):
        return self.proprietaire.nom +", " + self.proprietaire.prenom + "-" +  self.batiment.rue +", " + self.batiment.localite

    def get_absolute_url(self):
        return reverse('proprietaire_list')

    class Meta:
        unique_together = (("proprietaire", "batiment"),)


class ContratLocation(models.Model):
    batiment             = models.ForeignKey(Batiment)
    date_debut           = models.DateField(auto_now = False,  auto_now_add = False, verbose_name=u"Date début")
    date_fin             = models.DateField(auto_now = False, auto_now_add = False, blank = True, null = True)
    renonciation         = models.DateField(auto_now = False, auto_now_add = False, blank = True, null = True)
    remarque             = models.TextField(blank = True, null = True)
    assurance            = models.ForeignKey('Assurance', blank = True, null = True)
    loyer_base   = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    charges_base = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    #index_base   = models.DecimalField(max_digits=5, decimal_places=2, default = 0)

    def __str__(self):
        desc=""
        if not(self.batiment.description is None):
            desc+= self.batiment.description
        if not(self.batiment.localite is None):
            desc+= self.batiment.localite
        if not(self.date_debut is None):
            desc+= self.date_debut.strftime('%d-%m-%Y')
        if not(self.date_fin is None):
            desc+= " au " + self.date_fin.strftime('%d-%m-%Y')
        return desc
    @property
    def locataires(self):
        return Locataire.objects.filter(contrat_location=self)

    @property
    def financement_courant(self):
        list= FinancementLocation.objects.filter(contrat_location=self)\
                                           .order_by('date_fin')
        for f in list:
            return f
        return None


    def financements(self):
        return FinancementLocation.objects.filter(contrat_location=self)

    def save(self,  *args, **kwargs):
        print('contrat location save' ,self.id)
        date_fin = self.date_fin
        nouveau = False
        if self.id is None:
            nouveau = True
        c=super(ContratLocation, self).save(*args, **kwargs)
        if nouveau:
            print('creation nouveau financement')
            b = FinancementLocation(date_debut=self.date_debut,date_fin=self.date_fin, loyer=self.loyer_base)
            b.contrat_location = self
            b.save()

            date_d = self.date_debut
            date_f = self.date_debut + relativedelta(months=1)
            i=0
            while date_f <= date_fin:
                print(' creation nouveau suivi')
                suivi = SuiviLoyer(etat_suivi='A_VERIFIER', date_paiement=date_d, remarque=None,loyer_percu = 0,charges_percu=0)
                suivi.financement_location = b
                suivi.save()
                date_d = date_d + relativedelta(months=1)
                date_f = date_f + relativedelta(months=1)
                i=i+1
            if self.date_fin:
                alert = Alerte(description='Attention fin contrat location dans 1 mois',date_alerte=self.date_fin - relativedelta(months=1),etat='A_VERIFIER',contratLocation=self)
                alert.save()

        return c

    # def get_absolute_url(self):
    #     return reverse('contratlocation_list')

    class Meta:
        ordering = ['date_debut']


class FinancementLocation(models.Model):
    contrat_location = models.ForeignKey(ContratLocation,default=None)
    date_debut       = models.DateField(auto_now = False, auto_now_add = False, verbose_name=u"Date début")# je n'arrive pas à mettre la date du jour par défaut
    date_fin         = models.DateField(auto_now = False, auto_now_add = False, blank = True, null = True)
    loyer            = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    charges          = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    index            = models.DecimalField(max_digits=5, decimal_places=2, default = 0)

    def __str__(self):
        chaine = str(self.loyer) + "/" + str(self.charges)
        if self.date_debut is not None :
            chaine = chaine + " (" + self.date_debut.strftime('%d-%m-%Y')
        if self.date_fin is not None :
            chaine = chaine + " au " + self.date_fin.strftime('%d-%m-%Y') +")"

        return chaine


class Locataire(models.Model):
    personne             = models.ForeignKey(Personne,error_messages={'unique': 'Please enter your name'})
    contrat_location     = models.ForeignKey(ContratLocation,default=None)
    infos_complement     = models.TextField(blank = True, null = True)
    principal            = models.BooleanField(default = True)
    societe              = models.CharField(max_length=100, blank = True, null = True, verbose_name=u"Société")
    tva                  = models.CharField(max_length=30, blank = True, null = True)
    profession           = models.CharField(max_length=50, blank = True, null = True)
    #personne_garante     = models.ForeignKey('Personne', blank = True, null = True)

    def __str__(self):
        #return self.personne.nom + ", " + self.personne.prenom + " (" + self.financement_location.date_debut.strftime('%d-%m-%Y') + " au " + self.financement_location.date_fin.strftime('%d-%m-%Y') + ")"
        return self.personne.nom + ", " + self.personne.prenom

    # def unique_error_message(self, model_class, unique_check):
    #     print('uni')
    #     if model_class == type(self) and unique_check == ('personne', 'contrat_location'):
    #         return "kkk"
    #     else:
    #         return super(Locataire, self).unique_error_message(model_class, unique_check)
    #
    class Meta:
        unique_together = (("personne", "contrat_location"),)


class Societe(models.Model):
    nom                    = models.CharField(max_length = 100, blank=False, null=False)
    description            = models.TextField(blank = True, null = True)
    rue                    = models.CharField(max_length = 200, blank = True, null = True)
    numero                 = models.IntegerField(blank = True, null = True)
    boite                  = models.CharField(max_length = 10, blank = True, null = True)
    lieu_dit               = models.CharField(max_length = 200, blank = True, null = True)
    code_postal            = models.CharField(max_length = 10, blank = True, null = True)
    localite               = models.CharField(max_length = 150, blank = True, null = True)
    personnel              = models.ForeignKey(Personne, blank = True, null = True)

    def __str__(self):
        return self.nom


class FraisMaintenance(models.Model):
    proprietaire     = models.ForeignKey(Proprietaire, verbose_name=u"Propriétaire")
    entrepreneur     = models.ForeignKey(Personne, blank = True, null = True)
    societe          = models.ForeignKey(Societe, blank = True, null = True)
    description      = models.TextField()
    montant          = models.DecimalField(max_digits=8, decimal_places=2, default = 0)
    date_realisation = models.DateField(auto_now = False, auto_now_add = False, blank = True, null = True, verbose_name=u"Date réalisation")

    def __str__(self):
        return self.proprietaire.proprietaire.nom + ", " + self.proprietaire.proprietaire.prenom  + " " + self.proprietaire.batiment.rue +" "+ self.description


class SuiviLoyer(models.Model):
    ETAT = (
        ('A_VERIFIER','A vérifier'),
        ('IMPAYE','Impayé'),
        ('EN_RETARD','En retard'),
        ('PAYE','Payé')
    )
    financement_location = models.ForeignKey(FinancementLocation)
    date_paiement        = models.DateField(auto_now = False,auto_now_add = False)
    etat_suivi           = models.CharField(max_length = 10, choices = ETAT, default = 'A_VERIFIER')
    remarque             = models.TextField(blank = True, null = True)
    loyer_percu          = models.DecimalField(max_digits=5, decimal_places=2, blank = True, null = True)
    charges_percu        = models.DecimalField(max_digits=5, decimal_places=2 , blank = True, null = True)

    class Meta:
        ordering = ['date_paiement']

    def find_suivis(date_d, date_f, etat):
        if etat is None:
            return SuiviLoyer.objects.filter(date_paiement__gte = date_d, date_paiement__lte = date_f)
        else:
            return SuiviLoyer.objects.filter(date_paiement__gte = date_d, date_paiement__lte = date_f, etat_suivi = etat)

    def __str__(self):
        desc = ""
        if not(self.date_paiement is None):
            desc += self.date_paiement.strftime('%d-%m-%Y')

        if not(self.remarque is None):
            desc +=  " , (" + self.remarque + ")"

        if not(self.etat_suivi is None):
            desc +=   " (" + self.etat_suivi + ")"
        return desc


class ContratGestion(models.Model):
    batiment     = models.ForeignKey(Batiment)
    gestionnaire = models.ForeignKey(Personne)
    date_debut   = models.DateField(auto_now = False,  auto_now_add = False,blank=True, null=True)
    date_fin     = models.DateField(auto_now = False, auto_now_add = False, blank = True, null = True)

    def __str__(self):
        return self.gestionnaire.nom + ", " + self.gestionnaire.prenom  + str(self.batiment)
    #
    # def get_absolute_url(self):
    #     return reverse('contratgestion_list')

    def save(self,  *args, **kwargs):

        c=super(ContratGestion, self).save(*args, **kwargs)

        if self.date_fin :
            alert = Alerte(description='Attention fin contrat location dans 1 mois',date_alerte=self.date_fin - relativedelta(months=1),etat='A_VERIFIER',contratGestion=c)
            alert.save()
        return c

class ModeleDocument(models.Model):
    # TYPE_DOCUMENT = (
        # ('LETTRE_INDEXATION','Lettre indexation'),
    # )
    type_document = models.CharField(max_length = 50)
    contenu       = models.TextField()

    def __str__(self):
        return self.type_document

class Alerte(models.Model):
    ETAT = (
        ('A_VERIFIER','A vérifier'),
        ('VERIFIER','Vérifier'),
        ('COURRIER','Courrier à préparer'))

    description =  models.TextField( verbose_name=u"Description")
    date_alerte = models.DateField(auto_now = False, auto_now_add = False, blank = True, null = True, verbose_name=u"Date alerte")
    contratGestion = models.ForeignKey(ContratGestion, blank = True, null = True, verbose_name=u"Contrat de gestion")
    contratLocation = models.ForeignKey(ContratLocation, blank = True, null = True, verbose_name=u"Contrat location")
    etat = models.CharField(max_length = 10, choices = ETAT, default = 'A_VERIFIER', verbose_name=u"Etat")

    class Meta:
        ordering = ['date_alerte']

    def find_by_etat(etat_alerte):
        return Alerte.objects.filter(etat=etat_alerte)


class Pays(models.Model):
    pays = models.CharField(max_length = 50)


class Localite(models.Model):
    code_postal            = models.CharField(max_length = 10, blank = True, null = True)
    localite               = models.CharField(max_length = 150, blank = True, null = True)
