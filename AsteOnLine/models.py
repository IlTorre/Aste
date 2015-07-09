# -*- coding: utf-8 -*
from django.db import models
from django.contrib.auth.models import User,AbstractUser,PermissionsMixin
from django.utils import timezone
import datetime
import os
from django.conf import settings
# Create your models here.

class MyUser (AbstractUser):
    """
    Classe che estende la classe user di Django per aggiungere il campo indirizzo al modello del db
    """
    indirizzo=models.TextField(max_length=200)


def get_catName(istanza,file):
    """
    Crea il path in cui salvare i le immagini di categoria
    Per evitare conflitti i file vengono salvati nella cartella media/foto_categorie/{data di caricamento}/{ora di caricamento}.estensione
    :param istanza: l'istanza chiamante
    :param file: il file da salvare
    :return: il path di salvataggio
    """
    return os.path.join('foto_categorie',
                        str(timezone.datetime.date(timezone.now())),
                        str(timezone.datetime.time(timezone.now())).replace(':','_').replace('.','_')+os.path.splitext(file)[1])

class Categoria (models.Model):
    """
    Modello che implementa una categoria del db
    """
    nome = models.CharField(max_length=20, unique=True)
    foto = models.ImageField(upload_to=get_catName, default=settings.NO_MEDIA)
    descrizione = models.TextField(max_length=300)

    def __unicode__(self):
        return self.nome

    class Meta:
        """
        Classe delle metainformazioni: definisce il plurale
        """
        verbose_name_plural = 'Categorie'

def get_nome (istanza,file):
    """
    Crea il path in cui salvare i le immagini delle aste caricate dagli utenti
    Per evitare conflitti i file vengono salvati nella cartella media/uploaded_files/{utente}/{data di caricamento}/{ora di caricamento}.estensione
    :param istanza: l'istanza chiamante
    :param file: il file da salvare
    :return: il path
    """
    return os.path.join('uploaded_files',
                        str(istanza.creatore),
                        str(timezone.datetime.date(timezone.now())),
                        str(timezone.datetime.time(timezone.now())).replace(':','_').replace('.','_')+os.path.splitext(file)[1]
                        )


SCELTE_STATO=(('In preparazione','In preparazione'),('Spedito','Spedito'),('Ricevuto','Ricevuto'))
class Asta (models.Model):
    """
    Modello che implementa l'asta nel db
    """
    creatore = models.ForeignKey(MyUser)
    titolo = models.CharField(max_length=140)
    descrizione = models.TextField(max_length=900)
    foto = models.ImageField(upload_to=get_nome, default=settings.NO_MEDIA)
    data_apertura = models.DateTimeField(default=timezone.now)
    data_chiusura = models.DateTimeField(default=timezone.now()+datetime.timedelta(days=1))
    categoria= models.ForeignKey(Categoria)
    base_asta = models.DecimalField(max_digits=8,decimal_places=2,default=0.10)
    offerta_corrente = models.DecimalField(max_digits=8,decimal_places=2,default=0.00)
    stato = models.CharField(max_length=15, choices=SCELTE_STATO, default=SCELTE_STATO[0])

    def image_tag(self):
        """
        Funzione che implementa la visualizzazione della foto dell'asta.
        Viene usata nell'interfaccia di admin per mostrare le foto.
        :return: html che visualizza la foto
        """
        return u'<p align ="center"><img src="%s" width ="100px" align ="middle"/></p>' % self.foto.url
    image_tag.short_description = 'Foto'
    image_tag.allow_tags = True
    class Meta:
        """
        Classe delle metainformazioni: definisce il plurale
        """
        verbose_name_plural = 'Aste'
    def __unicode__(self):
        return str(self.titolo)+" - "+str(self.creatore)

    def attiva(self):
        """
        funzione che ritorna ce un asta è ancor attiva (è possibile votare per quell'asta, non è scaduta)
        :return: un valore booleano che definisce se è attiva
        """
        return self.data_chiusura>timezone.now()

    attiva.admin_order_field = '-data_chiusura'
    attiva.boolean = True
    attiva.short_description = 'Attiva?'

class Puntata (models.Model):
    """
    Classe che implementa la puntata nel db.
    """
    importo = models.DecimalField(max_digits=8,decimal_places=2)
    data = models.DateTimeField(default=timezone.now)
    utente = models.ForeignKey(MyUser)
    asta = models.ForeignKey(Asta)

    class Meta:
        """
        Classe delle metainformazioni: definisce il plurale e i campi univoci nel modello
        """
        verbose_name_plural = 'Puntate'
        unique_together=('importo','asta')
