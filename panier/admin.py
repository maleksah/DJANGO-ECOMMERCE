from django.contrib import admin
from panier.models import Panier, ProduitsPanier

class ProduitsPanierAdmin(admin.ModelAdmin):
    list_display = ('panier','produit','quantite')

admin.site.register(Panier)
admin.site.register(ProduitsPanier, ProduitsPanierAdmin)