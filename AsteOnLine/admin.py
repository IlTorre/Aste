from django.contrib import admin
from .models import Asta,Categoria


admin.site.register(Categoria)

class TutteAste (admin.ModelAdmin):
    fieldsets = [
        ('Utente:',{'fields':['creatore']}),
        ('Descrizione asta:',{'fields':['titolo','foto','descrizione','categoria']}),
        ('Opzioni asta:',{'fields':['base_asta','data_apertura','data_chiusura']})
    ]
    readonly_fields = ( 'image_tag', )
    list_display = ('image_tag','titolo','creatore','data_apertura','data_chiusura','attiva','base_asta')
    ordering = ['-data_chiusura','data_apertura']

admin.site.register(Asta,TutteAste)