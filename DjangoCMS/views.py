# -*- coding: utf-8 -*-
# Create your views here.

from django.shortcuts import redirect, render
from articles.models import Produit

def accueil(request):
    products = Produit.objects.filter(quantite_dispo__gt=0)
    best_sells = products.order_by('quantite_vendue').reverse()[:3]
    new_products = products.order_by('id').reverse()[:4]
    return render(request, 'index.html',{'best_sells':best_sells, 'new_products':new_products})


