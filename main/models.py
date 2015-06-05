from django.db import models

class Batiment(models.Model):
    denomination  = models.TextField(max_length=100)
    rue           = models.CharField(max_length=150)
	code_postal   = models.CharField(max_length=10)
	localite      = models.CharField(max_length=100)
	peb           = models.DecimalField(max_digits=6, decimal_places=2)
	surface       = models.DecimalField(max_digits=5, decimal_places=3)
	description   = models.TextField(max_length=500)
	#date_modif    = models.DateTimeField(auto_now=true,auto_now_add=true)
	#proprietaire  = models.ForeignKey('Personne')
    #loyer = models.DecimalField(max_digits=6, decimal_places=2)
	#charges = models.DecimalField(max_digits=5, decimal_places=2)
	#precompte_immobilier = DecimalField(max_digits=5, decimal_places=2)
	#credit_banque = models.ForeignKey('Banque')
	#credit_montant_total = models.DecimalField(max_digits=6, decimal_places=2)
	#credit_montant_achat = models.DecimalField(max_digits=6, decimal_places=2)
	#credit_montant_travaux = models.DecimalField(max_digits=6, decimal_places=2)
	#credit_montant_mensualite = models.DecimalField(max_digits=6, decimal_places=2)
	#credit_date_debut = models.DateField(auto_now=false,auto_now_add=false)
	#credit_date_fin = models.DateField(auto_now=false,auto_now_add=false)
	#assurance_proprietaire = models.ForeignKey('Assurance')

class Assurance(models.Model):
    nom         = models.CharField(max_length = 100)
    description = models.TextField(max_length = 255)

class Banque(models.Model):
    nom = models.CharField(max_length=100)

class Personne(models.Model):
	#CIVILITES = (
    #    ('Mr', 'Monsieur'),
    #    ('Mme', 'Madame'),
    #    ('Mlle', 'Mademoiselle'),
	#	('Me', 'Maitre'),
	#	('Dr', 'Docteur'),
    #)
    nom            = models.CharField(max_length=100)
	prenom         = models.CharField(max_length=100)
	email          = models.CharField(max_length=100)
	profession     = models.CharField(max_length=100)
	date_naissance = models.DateField(auto_now = false, auto_now_add = false)
	lieu_naissance = models.CharField(max_length=100)
	pays_naissance = models.CharField(max_length=100)
	num_identite   = models.CharField(max_length=100)
	telephome      = models.CharField(max_length=30)
	gsm            = models.CharField(max_length=30)
    #civilite = models.CharField(max_length=4,blank=true,choices=CIVILITES)

    def enregistrer(self):
        self.save()

    def __str__(self):
        return self.nom.upper() + ", " + self.prenom;

class Location(models.Model):
    batiment           = models.ForeignKey('Batiment')
    date_debut         = models.DateField(auto_now=true,auto_now_add=false)
    date_fin           = models.DateField(auto_now=false,auto_now_add=false)
    charges            = models.DecimalField(max_digits=5, decimal_places=2)
    assurance          = models.ForeignKey('Assurance')
    # bail_type           = models.CharField(max_length=100)
    # bail_duree          = models.CharField(max_length=100)
    # bail_unite          = models.CharField(max_length=100)
	# bail_jour_quittance = models.CharField(max_length=15)
	# bail_renom          = models.CharField(max_length=30)
	# bail_loyer = models.DecimalField(max_digits=5, decimal_places=2)
	# locataire_actif = models.BooleanField(default=true)
    # date_de_modif = models.DateTimeField(auto_now=true,auto_now_add=true)
    # index_ref = models.DecimalField(max_digits=5, decimal_places=2)
	# index_actuel= models.DecimalField(max_digits=5, decimal_places=2)

class Locataire(models.Model):
    personne             = models.ForeignKey('Personne')
	contrat              = models.ForeignKey('Location')
    societe              = models.CharField(max_length=100)
    num_tva              = models.CharField(max_length=30)
	profession_dans_bien = models.CharField(max_length=50)
    infos_complementaire = models.TextField(max_length=500)
    personne_garante     = models.ForeignKey('Personne')
	principal            = models.BooleanField(default=true)
    # nomReference = models.CharField(max_length=100)

class Depense(models.Model):
    batiment    = models.ForeignKey('Batiment')
	contrat     = models.ForeignKey('Location')
	description = models.TextField(max_length=500)
    montant     = models.DecimalField(max_digits=5, decimal_places=2)

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

class SuiviLoyer(models.Model)    :
    location           = models.ForeignKey('Location')
	revision           = models.ForeignKey('Revision')
    date_loyer_attendu = models.DateField(auto_now=false,auto_now_add=false)
    date_loyer_percu   = models.DateField(auto_now=false,auto_now_add=false)
    etat_suivi         = models.TextField(max_length=30)
	remarque           = models.TextField(max_length=500)
    date_de_modif      = models.DateTimeField(auto_now=true,auto_now_add=true)
    loyer_percu        = models.DecimalField(max_digits=5, decimal_places=2)
	charges_percu      = models.DecimalField(max_digits=5, decimal_places=2)
    # public enum EtatSuivi {
    # A_VERIFIER(0,"A vérifier"),
    # IMPAYE(1,"Impaye"),
    # EN_RETARD(2,"En retard"),
    # PAYE(3,"PAYE");

class Alerte(models.Model)    :
    location = models.ForeignKey('Location')
	message  = models.TextField(max_length=500)
    etat     = models.TextField(max_length=30)
	# mois_alerte = models.IntegerField()
	# annee_alerte = models.IntegerField()
	# date_creation = models.DateTimeField(auto_now=false,auto_now_add=true)
    #public enum EtatAlerte{
    #VERIFIE("vérifié"),
    #A_VERIFIER("A vérifier");
