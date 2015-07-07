from django.contrib import admin
from .models import Asta,Categoria,Puntata,MyUser
from GestioneUtenti.models import key
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm,UserCreationForm

admin.site.register(Categoria)

class TutteAste (admin.ModelAdmin):
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
    list_display = ('asta','utente','data','importo')
    ordering = ['asta','-data']

class TokenAttivazione (admin.ModelAdmin):
    list_display = ('utente','key')

class CustomUserChangeForm (UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = MyUser


class CustomUserCreationForm (UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username','email','first_name','last_name','password','indirizzo','is_active','is_superuser')

class Utenti (UserAdmin):
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
