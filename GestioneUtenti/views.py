from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect, HttpResponse
from AsteOnLine.models import MyUser as User
from django.db import IntegrityError
from django.core.mail import send_mail
from AsteOnLine.models import Asta,Puntata,Categoria
from GestioneUtenti.models import key as key_tab
from django.core.urlresolvers import reverse
from forms import carica_foto
import datetime
from django.utils import timezone
from django.conf import settings
import string
import random

def mylogin(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/account')
            else:
                return render(request,'GestioneUtenti/login.html',{'messaggio':'Account inattivo!'})
        else:
            return render(request,'GestioneUtenti/login.html',{'messaggio':'Nome utente o password errati, riprova!'})
    else:
        if request.user.is_anonymous():
            return render(request,'GestioneUtenti/login.html')
        else:
            return HttpResponseRedirect('/account')

def stringa_random(length=15):
    """
    Genero una stringa di caratteri casuali di
    lunghezza `length`, se non specificato 8 caratteri
    """
    return "".join([random.choice(string.letters) for c in xrange(length)])


def registrazione(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password1']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        indirizzo=request.POST['indirizzo']
        if (username == '' or first_name=='' or last_name == '' or email  == '' or indirizzo == ''):
            utente = {'username':username,'first_name': first_name,'last_name': last_name,'email': email,'indirizzo':indirizzo,'messaggio':'Attenzione: compila tutti i campi obbligatori!'}
            return render(request,'GestioneUtenti/registrazione.html',utente)
        try:
            user = User.objects.create_user(username=username,email=email,password=password,
                                            first_name=first_name,last_name=last_name,indirizzo=indirizzo)
            user.is_active=False
            user.save()
            key=user.username+stringa_random()

            att = key_tab.objects.create(utente=user,key=key)
            subject = 'Attivazione account'
            link = reverse('GestioneUtenti:attivazione',kwargs={'key':key})
            message = 'Attiva il tuo account visitando:\n'+'http://127.0.0.1:8000'+link
            print(message)
            sender = 'noreply.asteonline@gmail.com'
            recipients=[email]
            send_mail(subject, message, sender, recipients)
            info={'titolo':'Utente registrato correttamente','corpo':'Verifica la mail per attivare il tuo account'}
            return render(request, 'GestioneUtenti/avviso.html',info)
        except IntegrityError:
            utente = {'first_name': first_name,'last_name': last_name,'email': email,'indirizzo':indirizzo,'messaggio':'Attenzione: username non valido!'}
            return render(request,'GestioneUtenti/registrazione.html',utente)
    else:
        if request.user.is_anonymous():
            return render(request,'GestioneUtenti/registrazione.html')
        else:
            return HttpResponseRedirect(reverse('GestioneUtenti:profilo'))

def mylogout (request):
    logout(request)
    return HttpResponseRedirect(reverse('GestioneUtenti:login'))


@login_required(login_url='/account/login')
def portal_main_page(request):
    return render_to_response('GestioneUtenti/profilo.html',{'request':request})

def attiva(request, key):
    att=get_object_or_404(key_tab,pk=key)
    utente = User.objects.get(pk=att.utente.id)
    utente.is_active=True
    utente.save()
    att.delete()
    info={'titolo':'Account attivato con successo','corpo':'Da adesso in poi puoi navigare liberamente'}
    return render(request,'GestioneUtenti/avviso.html',info)

@login_required(login_url='/account/login')
def riepilogo(request):
    utente=request.user
    myaste=Asta.objects.filter(creatore=utente)
    ast=myaste.values()
    p=[]
    for i in xrange(len(myaste)):
        a=ast[i]
        print a
        if a['data_chiusura']<=timezone.now():
            a['data_chiusura']='Scaduta'
        try:
            a['vincente']=Puntata.objects.filter(asta=myaste[i]).last().utente.username
        except AttributeError:
            a['vincente']=""
        p.append(a)
    puntate=Puntata.objects.filter(utente=utente).order_by('-data')
    dettagli=[]
    for punt in puntate:
        det={}
        astx=punt.asta
        det['offerta_corrente']=Puntata.objects.filter(asta=astx).last().importo
        det['titolo']= punt.asta.titolo
        det['puntata']=punt.importo
        if punt.asta.data_chiusura <= timezone.now():
            det['scadenza']='Scaduta'
        else:
            det['scadenza']=punt.asta.data_chiusura
        det['vincente']= det['puntata'] == det['offerta_corrente']
        det['id_asta']=punt.asta.pk
        det['stato']=punt.asta.stato
        dettagli.append(det)

    context={'myaste':p, 'puntate':dettagli}
    return render(request, 'GestioneUtenti/riepilogo.html',context)

@login_required(login_url='/account/login')
def nuovaAsta(request):
    if request.method == 'GET':
        form=carica_foto()
        return render(request, 'GestioneUtenti/nuova_asta.html',{'form':form})
    else:
        form= carica_foto(request.POST,request.FILES)
        if form.is_valid():
            asta=form.save(commit=False)
            asta.creatore=request.user
            asta.base_asta=request.POST['base_asta']
            data_c=request.POST['data_chiusura']
            a,m,g=str(data_c).split('-')
            a=int(a)
            m=int(m)
            g=int(g)
            data_c=datetime.date(a,m,g)
            ora_c=request.POST['ora_chiusura']
            h,m=str(ora_c).split(':')
            h= int(h)
            m=int(m)
            ora_c=datetime.time(h,m)
            data=datetime.datetime.combine(data_c,ora_c)
            asta.data_chiusura=data
            asta.save()
            return HttpResponseRedirect(reverse('GestioneUtenti:riepilogo'))
        else:
            return render(request,'GestioneUtenti/nuova_asta.html',{'form':form,'messaggio':'Devi compilare i campi obbligatori'})
