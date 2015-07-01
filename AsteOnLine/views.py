from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib import auth
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Asta, Categoria,Puntata


class Home(generic.ListView):
    template_name = 'AsteOnLine/index.html'
    context_object_name = 'aste_recenti'
    def get_queryset(self):
        contenuto = Asta.objects.order_by('-data_chiusura')
        return contenuto[:10]

class Categorie (generic.ListView):
    template_name = 'AsteOnLine/categorie.html'
    context_object_name = 'categorie'
    def get_queryset(self):
        return Categoria.objects.all().order_by('nome')

@login_required(login_url='/account/login')
def offerta(request,id_asta):
    asta=get_object_or_404(Asta,pk=id_asta)
    if request.method=='POST':
        off=request.POST["offerta"]
        asta.offerta_corrente=off
        asta.save()
        puntata=Puntata.objects.create(asta=asta,utente=request.user,importo=off)
        puntata.save()

        return HttpResponseRedirect('/account/')

    else:
        return render(request,'AsteOnLine/dettaglio.html',{'asta':asta})

