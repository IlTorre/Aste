from django.shortcuts import render

# Create your views here.

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
from django.core.mail import send_mail
from forms import ContactForm, StatoForm
from .models import Asta, Categoria, Puntata, MyUser as User


class Home(generic.ListView):
    template_name = 'AsteOnLine/index.html'
    context_object_name = 'aste_recenti'
    def get_queryset(self):
        contenuto = Asta.objects.order_by('-data_chiusura')
        p=[]
        c=0
        for a in contenuto:
            if a.attiva():
                p.append(a)
                c=c+1
            if c >= 5:
                break

        return p

class Categorie (generic.ListView):
    template_name = 'AsteOnLine/categorie.html'
    context_object_name = 'categorie'
    def get_queryset(self):
        return Categoria.objects.all().order_by('nome')

def dettaglio_categoria(request,id_categoria):
    aste=Asta.objects.filter(categoria=id_categoria).order_by('-data_apertura')
    l=[]
    for a in aste:
        if a.attiva():
            l.append(a)
    categoria=get_object_or_404(Categoria,pk=id_categoria)

    context={'aste':l,'categoria':categoria}

    return render(request,'AsteOnLine/dettaglio_categoria.html',context)


def contatti (request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) #form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            subject = form.cleaned_data['oggetto']
            message = form.cleaned_data['messaggio']
            sender = form.cleaned_data['email']
            cc_myself = form.cleaned_data['invia_una_copia_a_me_stesso']
            recipients = ['noreply.asteonline@gmail.com']
            message=message+'\n\nModulo inviato da: '+sender
            if cc_myself:
                recipients.append(sender)
	    send_mail(subject, message, sender, recipients)
            context={'titolo':'Messaggio inviato','corpo':"La tua richiesta e' stata registrata."}
            return render(request,'GestioneUtenti/avviso.html',context) # Redirect after POST
        else:
	    return render(request,'AsteOnLine/contatti.html',{ 'form': form, 'messaggio':'Compila i campi obbligatori' })
    else:  # GET request: just visualize the form
        form = ContactForm() # An unbound form
        return render(request, 'AsteOnLine/contatti.html', { 'form': form })

def acquisti_correlati(id_acquisto):
    '''
    Ricava i suggerimenti di acquisto
    :param id_acquisto: e' l'id dell'oggetto osservato per il quale si vogliono ricavare le raccomandation
    :return: ritorna una lista di oggetti correlati
    '''
    utenti=Puntata.objects.filter(asta=Asta.objects.filter(pk=id_acquisto).last()).values_list('utente')

    utenti=set(utenti)

    l=[]
    for u in utenti:
        aste=Puntata.objects.filter(utente=u).values_list('asta')
        aste=set(aste)
        for i in aste:
            l.append(i)
    fin={}
    for k in l:
        kk=k[0]
        if kk in fin.keys():
            fin[kk][1]=fin[kk][1]+1
        else:
            fin[kk]=[kk,1]
    fin=fin.values()

    def confronto(x,y):
        return y[1]-x[1]

    fin.sort(cmp=confronto)
    l=[]
    for a in fin:
        l.append(a[0])

    return l


@login_required(login_url='/account/login')
def offerta(request,id_asta):
    asta=get_object_or_404(Asta,pk=id_asta)
    if request.method=='POST':
        if asta.attiva():
            off=request.POST["offerta"]
            if request.user == asta.creatore:
                info={'titolo':'Operazione non permessa','corpo':'Non puoi votare alle tue aste'}
                return render(request,'GestioneUtenti/avviso.html',info)
            elif asta.offerta_corrente >= float(off):
                info={'titolo':'Operazione non permessa','corpo':'Offerta minima non superata'}
                return render(request,'GestioneUtenti/avviso.html',info)
            else:

                asta.offerta_corrente=off
                asta.save()
                puntata=Puntata.objects.create(asta=asta,utente=request.user,importo=off)
                puntata.save()
        else:
            if request.user == asta.creatore:
                form=StatoForm(request.POST,instance=asta)
                form.save()
            else:
                info={'titolo':'Operazione non permessa','corpo':'Non puoi votare a un asta scaduta'}
                return render(request,'GestioneUtenti/avviso.html',info)

        return HttpResponseRedirect(reverse('GestioneUtenti:riepilogo'))
    else:
        diff=int((asta.data_chiusura-timezone.now()).total_seconds())
        form = StatoForm(instance=asta)
        attiva=asta.attiva()
        correlati=acquisti_correlati(id_asta)
        aste_correlate=[]
        utente=Puntata.objects.filter(asta=asta).last().utente
        for i in correlati:
            a=Asta.objects.get(pk=int(i))
            if a.attiva():
                aste_correlate.append(a)
        if len(aste_correlate)>0:
            try:
                aste_correlate.remove(Asta.objects.filter(pk=id_asta).last())
            except ValueError:
                pass

        return render(request,'AsteOnLine/dettaglio.html',{'asta':asta,'attiva':attiva,'correlati':aste_correlate,
                                                           'form':form,'restanti':diff,
                                                           'indirizzo':utente.first_name+' '+utente.last_name+ '\n'+utente.indirizzo})
