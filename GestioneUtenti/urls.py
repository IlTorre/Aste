from django.conf.urls import url
from . import views



urlpatterns = [
    url(r'^$', views.portal_main_page, name='profilo'),
    url(r'^login/$', views.mylogin, name='login'),
    url(r'^logout/$', views.mylogout, name='logout'),
    url(r'^registrazione/$',views.registrazione, name='registrazione'),
    url(r'^attiva/(?P<id_utente>[0-9]+)/$',views.attiva, name='attivazione')

    ]