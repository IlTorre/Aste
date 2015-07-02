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
from django.utils import timezone

from .models import Asta, Categoria,Puntata


class Home(generic.ListView):
    template_name = 'AsteOnLine/index.html'
    context_object_name = 'aste_recenti'
    def get_queryset(self):
        contenuto = Asta.objects.order_by('-data_chiusura')
        p=[]
        for a in contenuto:
            if a.attiva():
                p.append(a)

        return p[:10]

class Categorie (generic.ListView):
    template_name = 'AsteOnLine/categorie.html'
    context_object_name = 'categorie'
    def get_queryset(self):
        return Categoria.objects.all().order_by('nome')

@login_required(login_url='/account/login')
def offerta(request,id_asta):
    asta=get_object_or_404(Asta,pk=id_asta)
    if request.method=='POST':
        if request.user == asta.creatore:
            info={'titolo':'Operazione non permessa','corpo':'Non puoi votare alle tue aste'}
            return render(request,'GestioneUtenti/avviso.html',info)
        elif asta.data_chiusura < timezone.now():
            info={'titolo':'Operazione non permessa','corpo':'Non puoi votare a un asta scaduta'}
            return render(request,'GestioneUtenti/avviso.html',info)
        else:
            off=request.POST["offerta"]
            asta.offerta_corrente=off
            asta.save()
            puntata=Puntata.objects.create(asta=asta,utente=request.user,importo=off)
            puntata.save()
            return HttpResponseRedirect(reverse('GestioneUtenti:riepilogo'))
    else:
        attiva=asta.attiva()
        return render(request,'AsteOnLine/dettaglio.html',{'asta':asta,'attiva':attiva})

def dettaglio_categoria(request,id_categoria):
    aste=Asta.objects.filter(categoria=id_categoria).order_by('-data_apertura')
    l=[]
    for a in aste:
        if a.attiva():
            l.append(a)


    categoria=get_object_or_404(Categoria,pk=id_categoria)

    context={'aste':l,'categoria':categoria}

    return render(request,'AsteOnLine/dettaglio_categoria.html',context)
