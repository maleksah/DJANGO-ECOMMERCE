# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

class Produit(models.Model):
    libelle             = models.CharField(max_length=30)
    ref                 = models.CharField(max_length=20)
    slug                = models.SlugField(max_length=100) #pour l'utiliser dans l'url au lieu de l'id pourque l'utilisateur comprenne la signification depuis l'url
    poids               = models.FloatField(null=True, blank=True)
    description         = models.TextField(blank=True)
    date                = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date de parution")
    catalogue           = models.BooleanField(help_text="Cochez si vous vouler afficher le produit dans le catalogue") #Si on veut afficher le produit dans le catalogue ou non
    prix                = models.FloatField()
    quantite_vendue     = models.IntegerField(default=0)
    photo               = models.ImageField(upload_to="images/produits/imgPrincipales/")
    categorie           = models.ForeignKey('Categorie')
    quantite_dispo      = models.IntegerField()

    def __unicode__(self):
        return u"%s" % self.libelle

class Categorie(models.Model):
    libelle             = models.CharField(max_length=30)
    taxe                = models.FloatField()
    photo               = models.ImageField(upload_to="images/categories/")

    def __unicode__(self):
        return u"%s" % self.libelle






