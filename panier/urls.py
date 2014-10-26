from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns('panier.views',
    url(r'^$','afficher_panier'),
    url(r'^ajouter/(\d+)$','ajouter_produit'),
    url(r'^supprimer/(\d+)$','supprimer_produit_panier'),
    url(r'^payment/$','afficher_panier'),
    url(r'^return_url/$','return_url'),
    url(r'^cancel_return/$','cancel_return'),
    url(r'^increment_quantite_produit/$', 'increment_quantite_produit', name='increment_quantite_produit'),
     url(r'^decrement_quantite_produit/$', 'decrement_quantite_produit', name='decrement_quantite_produit'),
)