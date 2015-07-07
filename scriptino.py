from AsteOnLine.models import Asta,Categoria,Puntata
from django.contrib.auth.models import User
import random
def inserisci_utente(nome):
    User.objects.create_user(nome,None,nome)

def inserisci_asta(creatore, titolo, categoria, descrizione ):
    Asta.objects.create(creatore=creatore,titolo=titolo,descrizione=descrizione,categoria=categoria)

def inserisci_puntata (utente,importo,asta):
    Puntata.objects.create(utente=utente,asta=asta,importo=importo)

for i in xrange(15):
    nome_utente="utente"+str(i)
    inserisci_utente(nome_utente)
    for j in Categoria.objects.all():
        titolo_asta="asta"+str(j)+nome_utente
        inserisci_asta(nome_utente,titolo_asta,j,"prova")

for i in xrange(80):
    numero_utente = random(15)
    utente= User.objects.filter(username="Utente"+str(numero_utente)).last()
    asta =
