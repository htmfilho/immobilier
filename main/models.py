from django.db import models

class Client(models.Model):
    nom    = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email  = models.CharField(max_length=100)
    gsm    = models.CharField(max_length=20, null = True)
    fixe   = models.CharField(max_length=20, null = True)

    def enregistrer(self):
        self.save()

    def __str__(self):
        return self.nom.upper() + ", " + self.prenom;
