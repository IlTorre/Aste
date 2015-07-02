from django.forms import ModelForm
from AsteOnLine.models import Asta

class carica_foto (ModelForm):
    class Meta:
        model = Asta
        fields = ['foto','descrizione','titolo','categoria',]