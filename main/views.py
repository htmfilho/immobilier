from django.shortcuts import render
from main.models import Batiment, ContratLocation

# Create your views here.
def dashboard(request):    
    return render(request, 'main/dashboard.html', {})

def listeComplete(request):
    batiments = Batiment.objects.all()
    contrats_location = ContratLocation.objects.all()
    return render(request, 'main/listeComplete.html', {'batiments': batiments})
    
   
