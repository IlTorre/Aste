from django.db import models
from django.contrib.auth.models import User,AbstractUser,PermissionsMixin
from django.utils import timezone
import datetime
import os
from django.conf import settings
# Create your models here.

class MyUser (AbstractUser):
    indirizzo=models.TextField(max_length=200,default='Vuoto')


def get_catName(istanza,file):
    return os.path.join('foto_categorie',
                        str(timezone.datetime.date(timezone.now())),
                        str(timezone.datetime.time(timezone.now())).replace(':','_').replace('.','_')+os.path.splitext(file)[1])

class Categoria (models.Model):
    nome = models.CharField(max_length=20, unique=True)
    foto = models.ImageField(upload_to=get_catName, default=settings.NO_MEDIA)
    descrizione = models.TextField(max_length=300)

    def __unicode__(self):
        return self.nome
    class Meta:
        verbose_name_plural = 'Categorie'

def get_nome (istanza,file):
    return os.path.join('uploaded_files',
                        str(istanza.creatore),
                        str(timezone.datetime.date(timezone.now())),
                        str(timezone.datetime.time(timezone.now())).replace(':','_').replace('.','_')+os.path.splitext(file)[1]
                        )

SCELTE_STATO=(('In preparazione','In preparazione'),('Spedito','Spedito'),('Ricevuto','Ricevuto'))
class Asta (models.Model):
    creatore = models.ForeignKey(MyUser)
    titolo = models.CharField(max_length=140)
    descrizione = models.TextField(max_length=600)
    foto = models.ImageField(upload_to=get_nome, default=settings.NO_MEDIA)
    data_apertura = models.DateTimeField(default=timezone.now)
    data_chiusura = models.DateTimeField(default=timezone.now()+datetime.timedelta(days=1))
    categoria= models.ForeignKey(Categoria)
    base_asta = models.DecimalField(max_digits=8,decimal_places=2,default=0.10)
    offerta_corrente = models.DecimalField(max_digits=8,decimal_places=2,default=0.00)
    stato = models.CharField(max_length=15, choices=SCELTE_STATO, default=SCELTE_STATO[0])


    def image_tag(self):
        return u'<p align ="center"><img src="%s" width ="100px" align ="middle"/></p>' % self.foto.url
    image_tag.short_description = 'Foto'
    image_tag.allow_tags = True
    class Meta:
        verbose_name_plural = 'Aste'
    def __unicode__(self):
        return str(self.titolo)+" - "+str(self.creatore)
    def attiva(self):
        return self.data_chiusura>timezone.now()
    attiva.admin_order_field = '-data_chiusura'
    attiva.boolean = True
    attiva.short_description = 'Attiva?'

class Puntata (models.Model):
    importo = models.DecimalField(max_digits=8,decimal_places=2)
    data = models.DateTimeField(default=timezone.now)
    utente = models.ForeignKey(MyUser)
    asta = models.ForeignKey(Asta)

    class Meta:
        verbose_name_plural = 'Puntate'
        unique_together=('importo','asta')
