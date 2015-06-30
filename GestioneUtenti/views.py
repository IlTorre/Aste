from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
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
                print 'non attivo'
        else:
            print 'inesistente'
    else:
        return render(request,'GestioneUtenti/login.html')

@login_required(login_url='/account/login')
def portal_main_page(request):
    print request.user.first_name
    print 'Miki caccola'
    return render_to_response('GestioneUtenti/profilo.html',{'request':request})
