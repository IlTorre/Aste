# -*- coding: utf-8 -*
from django.forms import ModelForm
from AsteOnLine.models import Asta

class carica_foto (ModelForm):
    """
    Classe che implementa il form di caricamento di una asta
    """
    class Meta:
        """
        Classe delle metainformazioni che specifica il modello da utilizzare e i campi.
        """
        model = Asta
        fields = ['foto','descrizione','titolo','categoria',]