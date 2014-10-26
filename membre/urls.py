from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns('membre.views',
    url(r'^inscription/$','inscription'),
    url(r'^login/$','connexion'),
    url(r'^logout/$','deconnexion'),
    url(r'^profil/$','modifier_profil'),

)