from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import time
import os
from django.conf import settings
# Create your models here.

class Categoria (models.Model):
    nome = models.CharField(max_length=20, unique=True)
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

class Asta (models.Model):
    creatore = models.ForeignKey(User)
    titolo = models.CharField(max_length=140)
    descrizione = models.CharField(max_length=600)
    foto = models.ImageField(upload_to=get_nome, default=settings.NO_MEDIA)
    data_apertura = models.DateTimeField(default=timezone.now)
    data_chiusura = models.DateTimeField(default=timezone.now()+datetime.timedelta(days=7))
    categoria= models.ForeignKey(Categoria)
    base_asta = models.DecimalField(max_digits=8,decimal_places=2,default=0.10)
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
    utente = models.ForeignKey(User)
    asta = models.ForeignKey(Asta)

    class Meta:
        verbose_name_plural = 'Puntate'
        unique_together=('importo','asta')