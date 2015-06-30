from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db import IntegrityError

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

def registrazione(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password1']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        try:
            user = User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name)
            user.is_active=False
            user.save()
            info={'titolo':'Utente registrato correttamente','corpo':'Verifica la mail per attivare il tuo account'}
            return render(request, 'GestioneUtenti/avviso.html',info)
        except IntegrityError:
            utente = {'first_name': first_name,'last_name': last_name,'email': email,'messaggio':'Attenzione username non valido'}
            return render(request,'GestioneUtenti/registrazione.html',utente)
    else:
        if request.user.is_anonymous():
            return render(request,'GestioneUtenti/registrazione.html')
        else:
            return HttpResponseRedirect('/account')

def mylogout (request):
    logout(request)
    return render(request,'GestioneUtenti/login.html',{'messaggio':'Logout eseguito correttamente.'})


@login_required(login_url='/account/login')
def portal_main_page(request):
    return render_to_response('GestioneUtenti/profilo.html',{'request':request})

def attiva(request, id_utente):
    user = User.objects.get(pk=id_utente)
    user.is_active=True
    user.save()

    info={'titolo':'Account attivato con successo','corpo':'Da adesso in poi puoi navigare liberamente'}
    return render(request,'GestioneUtenti/avviso.html',info)
