# -*- coding: utf-8 -*-
from django import forms

default_errors = {
    'required': 'Veuillez remplir ce champ',
    'invalid': 'Entrez une valeur valide'
}

class ValiderCommandeForm(forms.Form):
    adresse_livraison             = forms.CharField(max_length=200,error_messages=default_errors,label="Adresse de livraison")
