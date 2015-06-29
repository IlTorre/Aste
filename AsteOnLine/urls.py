from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='index'),
    url(r'^asta(?P<pk>[0-9]+)/$', views.Dettaglio.as_view(), name='dettaglio'),
    url(r'^categorie$', views.Categorie.as_view(), name ='categorie'),
    url(r'^login$',views.login, name='login')
]