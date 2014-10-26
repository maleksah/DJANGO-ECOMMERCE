__author__ = 'Malek'

from entreprise.models import Entreprise
from articles.models import Categorie
from panier.models import ProduitsPanier
from articles.forms import RechercherProduitForm

def get_infos(request):
    entreprises = Entreprise.objects.all()
    if len(entreprises) > 0:
        entreprise = entreprises[0]
    else:
        entreprise = None

    categories_produits = Categorie.objects.all()
    total_panier = None
    nbr_produits_panier = None
    produits_panier = None
    if request.user.is_authenticated() and not request.user.is_staff:
        total_panier = 0
        nbr_produits_panier = 0
        produits_panier = ProduitsPanier.objects.filter(panier=request.user.panier)
        for produit_panier in produits_panier:
            nbr_produits_panier += produit_panier.quantite
            total_panier += produit_panier.quantite * produit_panier.produit.prix
    form_search = RechercherProduitForm()

    return {'entreprise':entreprise,'categories_produits':categories_produits,'total_panier':total_panier, 'produits_panier':produits_panier, 'nbr_produits_panier':nbr_produits_panier, 'form_search':form_search}
