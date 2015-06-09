from django.db import models


class Personne(models.Model):
    nom            = models.CharField(max_length = 100)
    prenom         = models.CharField(max_length = 100)
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

# class Batiment(models.Model):
    # denomination              = models.TextField(max_length = 100, blank = True, null = True)
    # rue                       = models.CharField(max_length = 150, blank = False, null = False)
    # code_postal               = models.CharField(max_length = 10, blank = True, null = True)
    # localite                  = models.CharField(max_length = 100, blank = False, null = False)
    # peformance_energetique    = models.DecimalField(max_digits = 6, decimal_places = 2)
    # surface                   = models.DecimalField(max_digits = 5, decimal_places = 3)
    # description               = models.TextField(max_length = 500, blank = True, null = True)
    # date_modif                = models.DateTimeField(auto_now = True)
    # proprietaire              = models.ForeignKey('Personne')
    # loyer                     = models.DecimalField(max_digits = 6, decimal_places = 2)
    # charges 	              = models.DecimalField(max_digits = 5, decimal_places = 2)
    # precompte_immobilier      = models.DecimalField(max_digits = 5, decimal_places = 2)
    # credit_banque             = models.ForeignKey('Banque')
    # credit_montant_total      = models.DecimalField(max_digits = 6, decimal_places = 2)
    # credit_montant_achat      = models.DecimalField(max_digits = 6, decimal_places = 2)
    # credit_montant_travaux    = models.DecimalField(max_digits = 6, decimal_places = 2)
    # credit_montant_mensualite = models.DecimalField(max_digits = 6, decimal_places = 2)
    # credit_date_debut         = models.DateField(auto_now = False, auto_now_add = False)
    # credit_date_fin           = models.DateField(auto_now = False, auto_now_add = False)
    # assurance_proprietaire    = models.ForeignKey('Assurance')
	
    # def __str__(self):
        # return self.denomination + ", " + localite


    # class Location(models.Model):
    #	batiment           = models.ForeignKey('Batiment')
    #	date_debut         = models.DateField(auto_now = True, auto_now_add = False)
    #  date_fin           = models.DateField(auto_now = False, auto_now_add = False)
    #  charges            = models.DecimalField(max_digits = 5, decimal_places=2)
    #  assurance          = models.ForeignKey('Assurance')
    # bail_type           = models.CharField(max_length = 100)
    # bail_duree          = models.CharField(max_length = 100)
    # bail_unite          = models.CharField(max_length = 100)
    # bail_jour_quittance = models.CharField(max_length = 15)
    # bail_renom          = models.CharField(max_length = 30)
    # bail_loyer = models.DecimalField(max_digits = 5, decimal_places=2)
    # locataire_actif = models.BooleanField(default = True)
    # date_modif = models.DateTimeField(auto_now = True)
    # index_ref = models.DecimalField(max_digits = 5, decimal_places=2)
    # index_actuel= models.DecimalField(max_digits = 5, decimal_places=2)
	# Il faudrait une clé vers une liste de locataire            = models.ForeignKey('Personne')

    # class Locataire(models.Model):
    #  personne             = models.ForeignKey('Personne')
    #  contrat              = models.ForeignKey('Location')
    #  societe              = models.CharField(max_length = 100)
    #  num_tva              = models.CharField(max_length = 30)
    #  profession_dans_bien = models.CharField(max_length = 50)
    #  infos_complementaires = models.TextField(max_length = 500)
    #  personne_garante     = models.ForeignKey('Personne')
    #  principal            = models.BooleanField(default = True)
    #	# nomReference = models.CharField(max_length = 100)
	#  location          = models.ForeignKey('Location')

    # class Depense(models.Model):
    #	batiment    = models.ForeignKey('Batiment')
    #	location     = models.ForeignKey('Location')
    #	description = models.TextField(max_length = 500)
    #	montant     = models.DecimalField(max_digits = 5, decimal_places=2)

    # class Revision(models.Model):
    #	location      = models.ForeignKey('Location')
    #	loyer         = models.DecimalField(max_digits = 5, decimal_places=2)
    #	charges       = models.DecimalField(max_digits = 5, decimal_places=2)
    #	index_actuel  = models.DecimalField(max_digits = 5, decimal_places=2)
    #   index_base    = models.DecimalField(max_digits = 5, decimal_places=2)
    #   date_debut    = models.DateField(auto_now = True, auto_now_add = False)
    #   date_fin      = models.DateField(auto_now = False, auto_now_add = False)
    #	remarque      = models.TextField(max_length = 500)
    #	etat_revision = models.TextField(max_length = 500)
    #   # public enum EtatRevision{
    #	# VERIFIE("Vérifié"),
    #	# A_VERIFIER("A vérifier"

    # class SuiviLoyer(models.Model)    :
    #	location           = models.ForeignKey('Location')
    #	revision           = models.ForeignKey('Revision')
    #	date_loyer_attendu = models.DateField(auto_now = False, auto_now_add = False)
    #	date_loyer_percu   = models.DateField(auto_now = False, auto_now_add = False)
    #	etat_suivi         = models.TextField(max_length = 30)
    #	remarque           = models.TextField(max_length = 500)
    #	date_modif         = models.DateTimeField(auto_now = True)
    #	loyer_percu        = models.DecimalField(max_digits = 5, decimal_places=2)
    #	charges_percu      = models.DecimalField(max_digits = 5, decimal_places=2)
    # public enum EtatSuivi {
    # A_VERIFIER(0,"A vérifier"),
    # IMPAYE(1,"Impaye"),
    # EN_RETARD(2,"En retard"),
    # PAYE(3,"PAYE");

    # class Alerte(models.Model)    :
    # location = models.ForeignKey('Location')
    # message  = models.TextField(max_length = 500)
    # etat     = models.TextField(max_length = 30)
    # mois_alerte = models.IntegerField()
    # annee_alerte = models.IntegerField()
    # date_creation = models.DateTimeField(auto_now = False, auto_now_add = True)
    # public enum EtatAlerte{
    # VERIFIE("vérifié"),
    # A_VERIFIER("A vérifier");
	
	# class Contrat(models.Model)    :
    # fournisseur = models.ForeignKey('Personne')
    # beneficiaire  = models.ForeignKey('Personne')
    # date_debut     = models.DateField(auto_now = True, auto_now_add = False)
    # date_fin     = models.DateField(auto_now = True, auto_now_add = False)
    # contrat = models.TextField(max_length = 500)
	# batiment = models.ForeignKey('Batiment', null = true)


