from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class key (models.Model):
    key = models.CharField(max_length=100,primary_key=True);
    utente = models.ForeignKey(User)