# -*- coding: utf-8 -*-
from django.shortcuts import redirect, render, render_to_response
from articles.models import Produit
from panier.models import ProduitsPanier
from django.http import HttpResponseRedirect, HttpResponse
from paypal.standard.forms import PayPalPaymentsForm
from django.core.urlresolvers import reverse
from commande.models import Commande, ProduitsCommande
from django.conf import settings
#from paypal.standard.ipn.models import PayPalIPN
from panier.forms import ValiderCommandeForm
from django.shortcuts import RequestContext
import json, datetime
from django.contrib.auth.decorators import login_required

@login_required
def ajouter_produit(request,id_produit):
    try:
        produit = Produit.objects.get(id=id_produit)
    except:
        return redirect('/')
    try:
        produit_panier = ProduitsPanier.objects.get(panier=request.user.panier, produit = produit)
        produit_panier.quantite += 1
        produit_panier.save()
    except:
        ProduitsPanier.objects.create(panier=request.user.panier, produit=produit,quantite=1)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) #Rediriger vers la page précédente

@login_required
def afficher_panier(request):
    #if request.user.is_authenticated():
    if request.method == 'POST':
        form = ValiderCommandeForm(request.POST) #Nous reprenons les donnees
        if form.is_valid():
            if len(request.user.panier.produits.all()) > 0:
                produits_panier = ProduitsPanier.objects.filter(panier=request.user.panier)
                erreur_disponibilite = False
                #Tester si les produits sont disponibles
                erreur_disponibilite_msg = ""
                for prod in produits_panier:
                    quantite_dispo = Produit.objects.get(id=prod.produit.id).quantite_dispo
                    if prod.quantite > quantite_dispo:
                        erreur_disponibilite = True
                        erreur_disponibilite_msg += "Il ne reste que " + str(quantite_dispo) + " article(s) de " + prod.produit.libelle + "\n"
                if not erreur_disponibilite:
                    adresse_livraison = form.cleaned_data['adresse_livraison']
                    try:
                        commande = Commande.objects.get(user=request.user, payee=False)
                        ProduitsCommande.objects.filter(commande=commande).delete()
                        commande.date_commande = datetime.datetime.now()
                    except:
                        commande = Commande.objects.create(user=request.user, payee=False, total=0, livree=False)
                        commande.save()
                    total = 0
                    commande.adresse_livraison = adresse_livraison

                    for prod_panier in produits_panier:
                        ProduitsCommande.objects.create(commande=commande, produit=prod_panier.produit, quantite=prod_panier.quantite)
                        total += prod_panier.quantite * prod_panier.produit.prix
                    commande.total = total
                    commande.save()

                    paypal_dict = {
                        "business": settings.PAYPAL_RECEIVER_EMAIL,
                        "amount": str(commande.total),
                        "currency_code" : "EUR",
                        "item_name": "Total de la commande",
                        "invoice": str(commande.id),
                        "notify_url": settings.SITE_URL+"/something/paypal/",
                        "return_url": settings.SITE_URL,
                        "cancel_return": settings.SITE_URL,
                    }
                    # Create the instance.
                    form_paiement = PayPalPaymentsForm(initial=paypal_dict)
                    context = {"form": form_paiement}
                    return render(request, "panier/paiement.html", locals())
    else:
        form = ValiderCommandeForm()
    return render(request,'panier/panier.html',locals())

@login_required
def increment_quantite_produit(request):
    print("increment_quantite_produit called !!!")
    context = RequestContext(request)
    produit_panier_id = None
    if request.method == 'GET':
        produit_panier_id = request.GET['id']
        total_panier = request.GET['total_panier']
        nbr_produits_panier = request.GET['nbr_produits_panier']
        print(total_panier)
    response_data = {}
    quantite = 0
    if produit_panier_id:
        produit_panier = ProduitsPanier.objects.get(id=int(produit_panier_id))
        if produit_panier:
            quantite = produit_panier.quantite + 1
            produit_panier.quantite = quantite
            produit_panier.save()
            response_data['quantite'] = quantite
            response_data['total'] = float(total_panier) + produit_panier.produit.prix
            response_data['nbr_produits_panier'] = int(nbr_produits_panier) +1
    return HttpResponse(json.dumps(response_data), content_type="application/json")
    #return render_to_response('panier/panier.html',context)

@login_required
def decrement_quantite_produit(request):
    print("decrement_quantite_produit called !!!")
    context = RequestContext(request)
    produit_panier_id = None
    if request.method == 'GET':
        produit_panier_id = request.GET['id']
        total_panier = request.GET['total_panier']
        nbr_produits_panier = request.GET['nbr_produits_panier']
        print(total_panier)
    response_data = {}
    quantite = 0
    if produit_panier_id and total_panier:
        produit_panier = ProduitsPanier.objects.get(id=int(produit_panier_id))
        if produit_panier:
            if produit_panier.quantite > 1:
                quantite = produit_panier.quantite - 1
                produit_panier.quantite = quantite
                produit_panier.save()
                response_data['quantite'] = quantite
                response_data['total'] = float(total_panier) - produit_panier.produit.prix
                response_data['nbr_produits_panier'] = int(nbr_produits_panier) - 1
            else:
                response_data['quantite'] = 1
                response_data['total'] = total_panier
                response_data['nbr_produits_panier'] = nbr_produits_panier
    return HttpResponse(json.dumps(response_data), content_type="application/json")
    #return render_to_response('panier/panier.html',context)

@login_required
def supprimer_produit_panier(request, id_produit):
    ProduitsPanier.objects.filter(produit=id_produit,panier=request.user.panier.id).delete()
    return redirect('/panier/')


def cancel_return(request):
    print("cancel_return called !!!!")
    return redirect('/')

def return_url(request):
    print("return_url called !!")
    return redirect('/')



