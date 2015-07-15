# -*- coding: utf-8 -*
from django.test import TestCase
from .models import Categoria,Puntata,Asta
from AsteOnLine.models import MyUser as User
from django.utils import timezone
import datetime
from django.core.urlresolvers import reverse
from django.test import Client

# Create your tests here.

def create_user(username='user'):
    """
    Crea un utente con username passato e password uguale al''username
    :param username: username dell'utente che si vuole creare
    :return: un utente
    """
    user = User.objects.create_user(username=username,password=username,indirizzo='Via Fasulla')
    return user

def create_asta(creatore,categoria,data_chiusura,titolo='Prova',descrizione='Descrizione di prova',base_asta=1):
    """
    Crea un asta da parametri passati
    :param titolo: titolo dell'asta
    :param descrizione: descrizione asta
    :param data_chiusura: data chiusura
    :param base_asta: offerta base
    :param creatore: utente creatore dell'asta
    :return: un asta
    """
    return Asta.objects.create(titolo=titolo,descrizione=descrizione,data_chiusura=data_chiusura,base_asta=base_asta,creatore=creatore,categoria=categoria)

def create_categoria(nome='Categoria Prova',descrizione='Desc prova'):
    """
    Crea una categoria

    :param nome: nome della categoria
    :param descrizione: descrizione categoria
    :return: una categoria
    """
    return Categoria.objects.create(nome=nome,descrizione=descrizione)


class QuestionMethodTests(TestCase):

    def test_asta_attiva(self):
        """
        Controllo che un asta con data di scadenza maggiore di oggi risulti attiva
        """
        creatore=create_user()
        cat = create_categoria()
        asta = create_asta(data_chiusura=timezone.now()+datetime.timedelta(days=1),creatore=creatore,categoria=cat)
        self.assertEqual(asta.attiva(), True)

    def test_asta_inattiva(self):
        """
        Controllo che un asta scaduta non risulti attiva
        """
        creatore=create_user()
        cat = create_categoria()
        asta = create_asta(data_chiusura=timezone.now()+datetime.timedelta(days=-1),creatore=creatore,categoria=cat)
        self.assertEqual(asta.attiva(), False)


class QuestionViewTests(TestCase):



    def test_asta_inesistente(self):
        """
        Controllo che venga ritornato un 404 in caso di asta inesistente
        """
        user = create_user('pippo')
        c = Client()
        c.login(username='pippo', password='pippo')
        response = c.get(reverse('AsteOnLine:offerta',kwargs={'id_asta':0}))
        self.assertEqual(response.status_code, 404)

    def test_asta_esistente(self):
        """
        Controllo che venga ritornata correttamente l'asta
        """
        user = create_user('pippo')
        c = Client()
        c.login(username='pippo', password='pippo')
        cat=create_categoria('prova','prova')
        asta=create_asta(user,cat,timezone.now()+datetime.timedelta(days=2))

        response = c.get(reverse('AsteOnLine:offerta',kwargs={'id_asta':asta.id}))
        self.assertEqual(response.status_code, 200)
        a=asta.titolo
        a2=[]
        for i in a:
            a2.append("'"+i+"'")
        self.assertQuerysetEqual(response.context['asta'].titolo.encode('ascii','ignore'),a2)
        self.assertEqual(response.context['attiva'],True)

    def test_puntate_asta_attiva (self):
        """
        controlla le operazioni di voto alle aste:
            un utente non puo' votare alle sue aste
            che l'inserimento corretto sia accettato
            un utente non puo' votare immettendo un importo monore rispetto l'ultima offerta fatta
        """
        user = create_user('pippo')
        c = Client()
        c.login(username='pippo', password='pippo')
        cat=create_categoria('prova','prova')
        asta=create_asta(user,cat,timezone.now()+datetime.timedelta(days=2))
        response = c.post(reverse('AsteOnLine:offerta',kwargs={'id_asta':asta.id}),{'offerta':10})
        self.assertEqual(response.context['titolo'],'Operazione non permessa')
        self.assertEqual(response.context['corpo'],'Non puoi votare alle tue aste')
        user2=create_user('pluto')
        asta = create_asta(user2,cat,timezone.now()+datetime.timedelta(days=2))
        response = c.post(reverse('AsteOnLine:offerta',kwargs={'id_asta':asta.id}),{'offerta':10})
        self.assertRedirects(response,reverse('GestioneUtenti:riepilogo'))
        response = c.post(reverse('AsteOnLine:offerta',kwargs={'id_asta':asta.id}),{'offerta':9})
        self.assertEqual(response.context['titolo'],'Operazione non permessa')
        self.assertEqual(response.context['corpo'],'Offerta minima non superata')

    def test_puntate_asta_inattiva (self):
        """
        Controlla che un utente non posa votare a un asta scaduta
        """
        user = create_user('pippo')
        user2 = create_user('pluto')
        c = Client()
        c.login(username='pippo', password='pippo')
        cat=create_categoria('prova','prova')
        asta=create_asta(user2,cat,timezone.now()+datetime.timedelta(days=-1))
        response = c.post(reverse('AsteOnLine:offerta',kwargs={'id_asta':asta.id}),{'offerta':10})
        self.assertEqual(response.context['titolo'],'Operazione non permessa')
        self.assertEqual(response.context['corpo'],'Non puoi votare a un asta scaduta')


    def test_articoli_correlati(self):
        """
        Controlla che se un utente vota per due ate compaia l'articolo correlato.
        """
        user = create_user('pippo')
        user2 = create_user('pluto')
        c = Client()
        c.login(username='pippo', password='pippo')
        cat=create_categoria('prova','prova')
        asta1=create_asta(user2,cat,timezone.now()+datetime.timedelta(days=2))
        asta2=create_asta(user2,cat,timezone.now()+datetime.timedelta(days=2))
        puntata=Puntata.objects.create(asta=asta1,utente=user,importo=10)
        puntata2=Puntata.objects.create(asta=asta2,utente=user,importo=10)
        response = c.get(reverse('AsteOnLine:offerta',kwargs={'id_asta':asta1.id}))
        self.assertEqual(response.context['correlati'][0].id,asta2.id)
