from django.contrib import admin
from .models import Asta,Categoria,Puntata,MyUser
from GestioneUtenti.models import key
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm,UserCreationForm

admin.site.register(Categoria)

class TutteAste (admin.ModelAdmin):
    """
    Classe che definisce la visualizzazione delle aste nel lato amministrativo
    """
    fieldsets = [
        ('Utente:',{'fields':['creatore']}),
        ('Descrizione asta:',{'fields':['titolo','foto','descrizione','categoria']}),
        ('Opzioni asta:',{'fields':['base_asta','data_apertura','data_chiusura','offerta_corrente']}),
        ('Stato spedizione:',{'fields':['stato']})
    ]
    readonly_fields = ( 'image_tag', )
    list_display = ('image_tag','titolo','creatore','data_apertura','data_chiusura','attiva','base_asta','offerta_corrente')
    ordering = ['-data_chiusura','data_apertura']

class TuttePuntate(admin.ModelAdmin):
    """
    Classe che definisce la visualizzazione delle puntate nel lato amministrativo
    """
    list_display = ('asta','utente','data','importo')
    ordering = ['asta','-data']

class TokenAttivazione (admin.ModelAdmin):
    """
    Classe che definisce la visualizzazione dei token di attivazione nel lato amministrativo
    """
    list_display = ('utente','key')

class CustomUserChangeForm (UserChangeForm):
    """
    Classe che definisce la modifica di un utente nel lato amministrativo
    """
    class Meta(UserChangeForm.Meta):
        model = MyUser


class CustomUserCreationForm (UserCreationForm):
    """
    Classe che definisce la creazione di un utente nel lato amministrativo
    """
    class Meta:
        model = MyUser
        fields = ('username','email','first_name','last_name','password','indirizzo','is_active','is_superuser')

class Utenti (UserAdmin):
    """
    Classe che definisce la visualizzazione degli utenti nel lato amministrativo
    """
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('username','email','indirizzo','is_active','is_superuser')

    fieldsets = [
        ('Informazioni Personali:',{'fields':['username','first_name','last_name','password','email','indirizzo']}),
        ('Informazioni generiche:',{'fields':['is_active','is_superuser']})
        ]



admin.site.register(MyUser,Utenti)
admin.site.register(Asta,TutteAste)
admin.site.register(Puntata,TuttePuntate)
admin.site.register(key,TokenAttivazione)
