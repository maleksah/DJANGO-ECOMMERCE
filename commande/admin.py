from django.contrib import admin
from commande.models import Commande, ProduitsCommande

class CommandeAdmin(admin.ModelAdmin):
    list_display = ('user','date_commande','payee','date_paiement','total','adresse_livraison','livree','date_livraison')
    list_editable = ('livree','date_livraison')
    date_hierarchy = 'date_paiement'

class ProduitsCommandeAdmin(admin.ModelAdmin):
    list_display = ('commande','produit','quantite')

admin.site.register(Commande, CommandeAdmin)
admin.site.register(ProduitsCommande, ProduitsCommandeAdmin)