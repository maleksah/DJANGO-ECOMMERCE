# -*- coding: utf-8 -*-
from django.db import models
from articles.models import Produit
from django.contrib.auth.models import User

class Panier(models.Model):
    user              = models.OneToOneField(User)
    produits            = models.ManyToManyField(Produit,through='ProduitsPanier')
    def __unicode__(self):
        return u"%s %s" % (self.user.last_name, self.user.first_name)


class ProduitsPanier(models.Model):
    panier              = models.ForeignKey(Panier)
    produit             = models.ForeignKey(Produit)
    quantite            = models.IntegerField()







