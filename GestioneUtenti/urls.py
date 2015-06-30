from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.portal_main_page, name='profilo'),
    url(r'^login/$', views.mylogin, name='mylogin'),
    ]