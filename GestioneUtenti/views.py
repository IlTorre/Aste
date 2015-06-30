from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect

# Create your views here.


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

def mylogout (request):
    logout(request)
    return render(request,'GestioneUtenti/login.html',{'messaggio':'Logout eseguito correttamente.'})


@login_required(login_url='/account/login')
def portal_main_page(request):
    return render_to_response('GestioneUtenti/profilo.html',{'request':request})
