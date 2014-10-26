# -*- coding: utf-8 -*-
# Create your views here.

from django.shortcuts import redirect, render, get_object_or_404
from articles.models import Categorie, Produit
from articles.forms import RechercherProduitForm

def articlesByCat(request,cat):
    produits = Produit.objects.filter(categorie__id=cat)
    categorie = Categorie.objects.get(id = cat)
    return render(request,'articles/articles_cat.html',{'produits':produits,'categorie':categorie})

def articleById(request,id, slug):
    produit = get_object_or_404(Produit,id=id, slug=slug)
    return render(request,'articles/detailsProduit.html',{'produit':produit})

def rechercher_produit(request):
    if request.method == 'POST':
        form = RechercherProduitForm(request.POST) #Nous reprenons les donnees
        if form.is_valid():
            mot_cle              = form.cleaned_data['mot_cle']
            produits_recherche = Produit.objects.filter(libelle__icontains=mot_cle)
            return render(request,'articles/resultat_recherche.html',{'produits_recherche':produits_recherche, 'mot_cle':mot_cle})
    return redirect("/")

