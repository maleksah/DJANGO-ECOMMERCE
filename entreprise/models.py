# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

class Entreprise(models.Model):
    nom                 = models.CharField(max_length=50)
    logo                = models.ImageField(upload_to="images/entreprise/logo/")
    telephone           = models.CharField( max_length=30)
    facebook            = models.CharField(blank=True, max_length=100)
    twitter             = models.CharField(blank=True, max_length=100)
    linkedin            = models.CharField(blank=True, max_length=100)
    skype               = models.CharField(blank=True, max_length=100)
    description         = models.TextField(blank=True)
    adresse             = models.CharField(max_length=100)
    email               = models.EmailField()

    def __unicode__(self):
        return u"%s" % self.nom




