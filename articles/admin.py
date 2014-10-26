from django.contrib import admin
from articles.models import Produit, Categorie

class ProduitAdmin(admin.ModelAdmin):
    list_display = ('libelle','prix','categorie', 'quantite_dispo', 'quantite_vendue')
    list_editable = ('quantite_dispo',)
    prepopulated_fields = {'slug':('libelle',), }


admin.site.register(Produit, ProduitAdmin)
admin.site.register(Categorie)
