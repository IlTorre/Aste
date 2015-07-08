from django import forms
from  AsteOnLine.models import Asta

class ContactForm(forms.Form):
    """
    Classe che implementa il form di contatto
    """
    oggetto = forms.CharField(max_length=100)
    messaggio = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    invia_una_copia_a_me_stesso = forms.BooleanField(required=False)

class StatoForm(forms.ModelForm):
    """
    Classe che implementa il form per la modifica dello stato della spedizione dell'ordine
    """
    class Meta:
        model = Asta
        fields = ['stato']