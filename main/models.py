from django.db import models
        
        
class Assurance(models.Model):
    nom         = models.CharField(max_length = 100)
    description = models.TextField(blank = True, null = True)

    def __str__(self):
        return self.nom

        
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
        
class Personne(models.Model):
    nom            = models.CharField(max_length = 100)
    prenom         = models.CharField(max_length = 100)
    societe        = models.CharField(max_length = 100, blank = True, null = True)
    email          = models.EmailField(blank = True, null = True)
    profession     = models.CharField(max_length = 100, blank = True, null = True)
    date_naissance = models.DateField(auto_now = False, blank = True, null = True, auto_now_add = False)
    lieu_naissance = models.CharField(max_length = 100, blank = True, null = True)
    pays_naissance = models.CharField(max_length = 100, blank = True, null = True)
    num_identite   = models.CharField(max_length = 100, blank = True, null = True)
    telephome      = models.CharField(max_length = 30, blank = True, null = True)
    gsm            = models.CharField(max_length = 30, blank = True, null = True)
    
    def __str__(self):
        return self.nom.upper() + ", " + self.prenom
        
    def find_personne(id):       
        return Personne.objects.get(pk=id)
        
class Batiment(models.Model):
    nom                    = models.CharField(max_length = 100)    
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
    photo                  = models.ManyToManyField(Photo, blank = True, null = True)
    
    
    def find_batiment(id):
        return Batiment.objects.get(pk=id)
        
    def __str__(self):
        return self.nom + ', ' + self.rue +  ', ' + self.localite
        
    def adresse_rue(self):
        adresse_complete=""
        if self.rue is not None :
            adresse_complete += self.rue
        if self.numero is not None :
            adresse_complete += " " +str(self.numero)                
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
    
class Proprietaire(models.Model):
    proprietaire  = models.ForeignKey(Personne)
    batiment      = models.ForeignKey(Batiment)
    date_debut    = models.DateField(auto_now = False, blank = True, null = True, auto_now_add = False)
    date_fin      = models.DateField(auto_now = False, blank = True, null = True, auto_now_add = False)
    
    def find_proprietaire(id):
        return Proprietaire.objects.get(pk=id)
        
    def batiments(self):        
        return Batiment.objects.filter(proprietaire=self) 
        
    def __str__(self):
        return self.proprietaire.nom +", " + self.proprietaire.prenom + "-" + self.batiment.nom + ", " + self.batiment.rue +", " + self.batiment.localite  

class ContratLocation(models.Model):
    batiment             = models.ForeignKey(Batiment)
       
    date_debut           = models.DateField(auto_now = False,  auto_now_add = False)
    date_fin             = models.DateField(auto_now = False, auto_now_add = False, blank = True, null = True)
    renonciation         = models.DateField(auto_now = False, auto_now_add = False, blank = True, null = True)
    remarque             = models.TextField(blank = True, null = True)
    assurance            = models.ForeignKey('Assurance', blank = True, null = True)
    #loyer_base   = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    #charges_base = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    #index_base   = models.DecimalField(max_digits=5, decimal_places=2, default = 0)  
   
    def __str__(self):
        return self.batiment.description + "," + self.batiment.localite + " (" + self.date_debut.strftime('%d-%m-%Y') + " - " + self.date_fin.strftime('%d-%m-%Y') + ")"
        
    def locataires(self):        
        return Locataire.objects.filter(contrat_location=self)    
        
    def financements(self):        
        return FinancementLocation.objects.filter(contrat_location=self)    

        
class FinancementLocation(models.Model):    
    contrat_location     = models.ForeignKey(ContratLocation,default=None)      
    date_debut = models.DateField(auto_now = False, auto_now_add = False)# je n'arrive pas à mettre la date du jour par défaut    
    date_fin   = models.DateField(auto_now = False, auto_now_add = False, blank = True, null = True)
    loyer      = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    charges    = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    index      = models.DecimalField(max_digits=5, decimal_places=2, default = 0)
    def __str__(self):
        chaine = str(self.loyer) + "/" + str(self.charges) 
        if self.date_debut is not None :
            chaine = chaine + " (" + self.date_debut.strftime('%d-%m-%Y') 
        if self.date_fin is not None :
            chaine = chaine + " au " + self.date_fin.strftime('%d-%m-%Y') +")"
            
        return chaine
        
        
        

      
class Locataire(models.Model):
    personne             = models.ForeignKey(Personne)
    contrat_location     = models.ForeignKey(ContratLocation,default=None)
    infos_complement     = models.TextField(blank = True, null = True)
    principal            = models.BooleanField(default = True)
    societe              = models.CharField(max_length=100, blank = True, null = True)
    tva                  = models.CharField(max_length=30, blank = True, null = True)
    profession           = models.CharField(max_length=50, blank = True, null = True)
    #personne_garante     = models.ForeignKey('Personne', blank = True, null = True)
    
    def __str__(self):
        #return self.personne.nom + ", " + self.personne.prenom + " (" + self.financement_location.date_debut.strftime('%d-%m-%Y') + " au " + self.financement_location.date_fin.strftime('%d-%m-%Y') + ")"
        return self.personne.nom + ", " + self.personne.prenom 

        
class FraisMaintenance(models.Model):
    proprietaire     = models.ForeignKey(Proprietaire)
    entrepreneur     = models.ForeignKey(Personne, blank = True, null = True)
    description      = models.TextField()
    montant          = models.DecimalField(max_digits=8, decimal_places=2, default = 0)
    date_realisation = models.DateField(auto_now = False, auto_now_add = False, blank = True, null = True)

    def __str__(self):
        return self.proprietaire.proprietaire.nom + ", " + self.proprietaire.proprietaire.prenom  + " " + self.proprietaire.batiment.nom +" "+ self.description 
       
       
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
    
    def __str__(self):
        return self.date_paiement.strftime('%d-%m-%Y') + " , (" + self.remarque + ")" + " (" + self.etat_suivi + ")"
           

class ContratGestion(models.Model):    
    batiment     = models.ForeignKey(Batiment)
    gestionnaire = models.ForeignKey(Personne)
    date_debut   = models.DateField(auto_now = True,  auto_now_add = False)
    date_fin     = models.DateField(auto_now = False, auto_now_add = False, blank = True, null = True)

    def __str__(self):
        return self.gestionnaire.nom + ", " + self.gestionnaire.prenom  + " - " + self.proprietaire.proprietaire.nom + ", " + self.proprietaire.proprietaire.prenom  
        
        
class ModeleDocument(models.Model):
    # TYPE_DOCUMENT = (
        # ('LETTRE_INDEXATION','Lettre indexation'),       
    # )  
    type_document = models.CharField(max_length = 50)
    contenu       = models.TextField()

    def __str__(self):
        return self.type_document   

        