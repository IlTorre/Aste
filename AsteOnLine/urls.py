from django.conf.urls import include, url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='index'),
    url(r'^asta(?P<pk>[0-9]+)/$', views.Dettaglio.as_view(), name='dettaglio'),
    url(r'^categorie$', login_required(views.Categorie.as_view(), login_url='/account/login'), name ='categorie'),
]