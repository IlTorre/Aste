from django.contrib import admin
from .models import Asta,Categoria,Puntata
from GestioneUtenti.models import key


admin.site.register(Categoria)

class TutteAste (admin.ModelAdmin):
    fieldsets = [
        ('Utente:',{'fields':['creatore']}),
        ('Descrizione asta:',{'fields':['titolo','foto','descrizione','categoria']}),
        ('Opzioni asta:',{'fields':['base_asta','data_apertura','data_chiusura','offerta_corrente']})
    ]
    readonly_fields = ( 'image_tag', )
    list_display = ('image_tag','titolo','creatore','data_apertura','data_chiusura','attiva','base_asta','offerta_corrente')
    ordering = ['-data_chiusura','data_apertura']

class TuttePuntate(admin.ModelAdmin):
    list_display = ('asta','utente','data','importo')
    ordering = ['asta','-data']

class TokenAttivazione (admin.ModelAdmin):
    list_display = ('utente','key')

admin.site.register(Asta,TutteAste)
admin.site.register(Puntata,TuttePuntate)
admin.site.register(key,TokenAttivazione)