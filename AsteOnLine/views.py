from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Asta


class Home(generic.ListView):
    template_name = 'AsteOnLine/index.html'
    context_object_name = 'aste_recenti'
    print 'ciao'

    def get_queryset(self):
        contenuto = Asta.objects.order_by('-data_chiusura')
        return contenuto

class Dettaglio(generic.DetailView):
    model = Asta
    template_name = 'AsteOnLine/dettaglio.html'
