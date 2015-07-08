# -*- coding: utf-8 -*
from django.db import models
from AsteOnLine.models import MyUser
# Create your models here.
class key (models.Model):
    """
    classe che implementa la chiave di attivazione dell'utente nel db
    """
    key = models.CharField(max_length=100,primary_key=True)
    utente = models.ForeignKey(MyUser)