from django.db import models


class Personne(models.Model):
    nom            = models.CharField(max_length = 100)
    prenom         = models.CharField(max_length = 100)
    societe        = models.CharField(max_length = 100, blank = True, null = True)
    email          = models.CharField(max_length = 100, blank = True, null = True)
    profession     = models.CharField(max_length = 100, blank = True, null = True)
    date_naissance = models.DateField(auto_now = False, blank = True, null = True, auto_now_add = False)
    lieu_naissance = models.CharField(max_length = 100, blank = True, null = True)
    pays_naissance = models.CharField(max_length = 100, blank = True, null = True)
    num_identite   = models.CharField(max_length = 100, blank = True, null = True)
    telephome      = models.CharField(max_length = 30, blank = True, null = True)
    gsm            = models.CharField(max_length = 30, blank = True, null = True)

    def __str__(self):
        return self.nom.upper() + ", " + self.prenom


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

        
class Batiment(models.Model):
    description            = models.TextField()
    nom                    = models.CharField(max_length = 100, blank = True, null = True)
    localite               = models.CharField(max_length = 150, blank = True, null = True)
    numero                 = models.IntegerField(blank = True, null = True)
    boite                  = models.CharField(max_length = 10, blank = True, null = True)
    code_postal            = models.CharField(max_length = 10, blank = True, null = True)
    ville                  = models.CharField(max_length = 100, blank = True, null = True)
    province               = models.CharField(max_length = 100, blank = True, null = True)
    surface                = models.DecimalField(max_digits = 5, decimal_places = 3, blank = True, null = True)
    peformance_energetique = models.CharField(max_length = 10,blank = True, null = True)

    def __str__(self):
        return self.description + ' (' + self.nom + ')'

        
class Proprietaire(models.Model):
    proprietaire  = models.ForeignKey('Personne')
    batiment      = models.ForeignKey('Batiment')
    date_debut    = models.DateField(auto_now = False, blank = True, null = True, auto_now_add = False)
    date_fin      = models.DateField(auto_now = False, blank = True, null = True, auto_now_add = False)
    # loyer = models.DecimalField(max_digits=6, decimal_places=2)
    # charges = models.DecimalField(max_digits=5, decimal_places=2)
    # precompte_immobilier = DecimalField(max_digits=5, decimal_places=2)
    # credit_banque = models.ForeignKey('Banque')
    # credit_montant_total = models.DecimalField(max_digits=6, decimal_places=2)
    # credit_montant_achat = models.DecimalField(max_digits=6, decimal_places=2)
    # credit_montant_travaux = models.DecimalField(max_digits=6, decimal_places=2)
    # credit_montant_mensualite = models.DecimalField(max_digits=6, decimal_places=2)
    # credit_date_debut = models.DateField(auto_now=false,auto_now_add=false)
    # credit_date_fin = models.DateField(auto_now=false,auto_now_add=false)
    # assurance_proprietaire = models.ForeignKey('Assurance')
    def __str__(self):
        return self.proprietaire.nom +", " + self.proprietaire.prenom + ' (' + self.batiment.nom + ')'
    
    
class Location(models.Model):
    batiment   = models.ForeignKey('Batiment')
    date_debut = models.DateField(auto_now = False, auto_now_add = False)# je n'arrive pas à mettre la date du jour par défaut
    date_fin   = models.DateField(auto_now = False, auto_now_add = False)
    loyer      = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    charges    = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    index      = models.DecimalField(max_digits=5, decimal_places=2, default = 0)
    assurance  = models.ForeignKey('Assurance', blank = True, null = True)

    def __str__(self):
        return self.batiment.nom + " (" + self.date_debut.strftime('%d-%m-%Y') + " au " + self.date_fin.strftime('%d-%m-%Y') + ")"
        
        
class Contrat(models.Model):
    location     = models.ForeignKey('Location')
    date_debut   = models.DateField(auto_now = True,  auto_now_add = False)
    date_fin     = models.DateField(auto_now = False, auto_now_add = False, blank = True, null = True)
    renonciation = models.DateField(auto_now = False, auto_now_add = False)
    loyer_base   = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    charges_base = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    index_base   = models.DecimalField(max_digits=5, decimal_places=2, default = 0)  
    # bail_jour_quittance = models.CharField(max_length=15) ?????
    
    def __str__(self):
        return self.location + " (" + self.date_debut + " - " + self.date_fin + ")"

        
class Locataire(models.Model):
    personne         = models.ForeignKey('Personne')
    location         = models.ForeignKey('Location')
    infos_complement = models.TextField(blank = True, null = True)
    principal        = models.BooleanField(default = True)
    societe          = models.CharField(max_length=100, blank = True, null = True)
    tva              = models.CharField(max_length=30, blank = True, null = True)
    profession       = models.CharField(max_length=50, blank = True, null = True)
    #personne_garante = models.ForeignKey('Personne')#??? rattaché à la location ou au locataire???
    
    def __str__(self):
        return self.personne.nom + ", " + self.personne.prenom + " (" + self.location.date_debut.strftime('%d-%m-%Y') + " au " + self.location.date_fin.strftime('%d-%m-%Y') + ")" + ")"

        
class FraisMaintenance(models.Model):
    proprietaire     = models.ForeignKey('Proprietaire')
    entrepreneur     = models.ForeignKey('Personne', blank = True, null = True)
    description      = models.TextField()
    montant          = models.DecimalField(max_digits=8, decimal_places=2, default = 0)
    date_realisation = models.DateField(auto_now = False, auto_now_add = False, blank = True, null = True)

    def __str__(self):
        return self.proprietaire.proprietaire.nom + ", " + self.proprietaire.proprietaire.prenom  + " " + self.proprietaire.batiment.nom +" "+ self.description 
        
        
    # class Revision(models.Model):
    #	location      = models.ForeignKey('Location')
    #	loyer         = models.DecimalField(max_digits=5, decimal_places=2)
    #	charges       = models.DecimalField(max_digits=5, decimal_places=2)
    #	index_actuel  = models.DecimalField(max_digits=5, decimal_places=2)
    #   index_base    = models.DecimalField(max_digits=5, decimal_places=2)
    #   date_debut    = models.DateField(auto_now=true,auto_now_add=false)
    #   date_fin      = models.DateField(auto_now=false,auto_now_add=false)
    #	remarque      = models.TextField(max_length=500)
    #	etat_revision = models.TextField(max_length=500)
    #   # public enum EtatRevision{
    #	# VERIFIE("Vérifié"),
    #	# A_VERIFIER("A vérifier"
class SuiviLoyer(models.Model):
    ETAT = (
        ('A_VERIFIER','A vérifier'),
        ('IMPAYE','Impayé'),
        ('EN_RETARD','En retard'),
        ('PAYE','Payé')
    )
    location      = models.ForeignKey('Location')    
    date_paiement = models.DateField(auto_now = False,auto_now_add = False)
    etat_suivi    = models.CharField(max_length = 10, choices = ETAT, default = 'A_VERIFIER')
    remarque      = models.TextField(blank = True, null = True)
    loyer_percu   = models.DecimalField(max_digits=5, decimal_places=2, blank = True, null = True)
    charges_percu = models.DecimalField(max_digits=5, decimal_places=2 , blank = True, null = True)
    
    def __str__(self):
        return self.location.batiment.nom + " (" + self.location.date_debut.strftime('%d-%m-%Y') + " au " + self.location.date_fin.strftime('%d-%m-%Y') + ")" + " (" + self.etat_suivi + ")"
        
    # class Alerte(models.Model)    : ???
    #	location = models.ForeignKey('Location')
    #	message  = models.TextField(max_length=500)
    #	etat     = models.TextField(max_length=30)
    # mois_alerte = models.IntegerField()
    # annee_alerte = models.IntegerField()
    # date_creation = models.DateTimeField(auto_now=false,auto_now_add=true)
    # public enum EtatAlerte{
    # VERIFIE("vérifié"),
    # A_VERIFIER("A vérifier");

class ContratGestion(models.Model):
    proprietaire = models.ForeignKey('Proprietaire')#??? 
    gestionnaire = models.ForeignKey('Personne')
    date_debut   = models.DateField(auto_now = True,  auto_now_add = False)
    date_fin     = models.DateField(auto_now = False, auto_now_add = False, blank = True, null = True)

    def __str__(self):
        return self.gestionnaire.nom + ", " + self.gestionnaire.prenom  + " - " + self.proprietaire.proprietaire.nom + ", " + self.proprietaire.proprietaire.prenom  