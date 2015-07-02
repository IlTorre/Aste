from django.conf.urls import include, url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='index'),
    url(r'^categorie$', login_required(views.Categorie.as_view(), login_url='/account/login'), name ='categorie'),
    url(r'^offerta/(?P<id_asta>[0-9]+)$',views.offerta,name='offerta'),
    url(r'^categorie/(?P<id_categoria>[0-9]+)$', views.dettaglio_categoria, name ='dettagliocategoria'),

]