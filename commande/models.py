# -*- coding: utf-8 -*-
from django.db import models
from articles.models import Produit
from django.contrib.auth.models import User

class Commande(models.Model):
    user                = models.ForeignKey(User)
    email_paiement      = models.EmailField(blank=True)
    produits            = models.ManyToManyField(Produit,through='ProduitsCommande')
    date_commande        = models.DateTimeField(auto_now_add=True, auto_now=False)
    payee               = models.BooleanField()
    date_paiement       = models.DateTimeField(blank=True, null=True)
    total               = models.FloatField()
    adresse_livraison   = models.CharField(max_length=200)
    livree              = models.BooleanField()
    date_livraison      = models.DateTimeField(blank=True, null=True)


    def __unicode__(self):
        return u"%s %s" % (self.user.last_name, self.user.first_name)


class ProduitsCommande(models.Model):
    commande              = models.ForeignKey(Commande)
    produit             = models.ForeignKey(Produit)
    quantite            = models.IntegerField()


from paypal.standard.ipn.signals import payment_was_successful

def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == "Completed":
        commande = Commande.objects.get(id=ipn_obj.invoice)
        if commande.total == ipn_obj.mc_gross and ipn_obj.mc_currency == "EUR":
            commande.email_paiement = ipn_obj.payer_email
            commande.payee = True
            commande.date_paiement = ipn_obj.payment_date
            commande.save()
            produits_commande = ProduitsCommande.objects.filter(commande=commande)
            for p in produits_commande:
                produit = p.produit
                produit.quantite_dispo -= p.quantite
                produit.quantite_vendue += p.quantite
                produit.save()
            ProduitsCommande.objects.filter(commande=commande).delete()



payment_was_successful.connect(show_me_the_money)
