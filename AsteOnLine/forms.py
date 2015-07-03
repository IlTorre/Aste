from django import forms

class ContactForm(forms.Form):
    oggetto = forms.CharField(max_length=100)
    messaggio = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    invia_una_copia_a_me_stesso = forms.BooleanField(required=False)