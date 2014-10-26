# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Membre(models.Model):
    user = models.OneToOneField(User)
    adress             = models.CharField(max_length=100)
    phone_number             = models.CharField(max_length=20)

    def __unicode__(self):
        return u"%s %s" % (self.user.first_name,self.user.last_name)

