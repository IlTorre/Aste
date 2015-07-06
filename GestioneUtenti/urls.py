from django.conf.urls import url
from . import views



urlpatterns = [
    url(r'^$', views.portal_main_page, name='profilo'),
    url(r'^login/$', views.mylogin, name='login'),
    url(r'^logout/$', views.mylogout, name='logout'),
    url(r'^registrazione/$',views.registrazione, name='registrazione'),
    url(r'^attiva/(?P<key>\w+)/$',views.attiva, name='attivazione'),
    url(r'^riepilogo/$',views.riepilogo, name='riepilogo'),
    url(r'^nuovaasta/$',views.nuovaAsta, name='nuovaasta')

    ]