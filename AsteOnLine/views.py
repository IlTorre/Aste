from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Asta


class IndexView(generic.ListView):
    template_name = 'AsteOnLine/index.html'
    context_object_name = 'aste_recenti'
    print 'ciao'
    def get_queryset(self):
        contenuto = 'lalala'#Asta.objects.all()
        print contenuto
        print 'puzzi'
        return contenuto