# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
import re

default_errors = {
    'required': 'Veuillez remplir ce champ',
    'invalid': 'Entrez une valeur valide'
}

class InscriptionForm(forms.Form):
    nom                 = forms.CharField(max_length=30,required=True,error_messages=default_errors)
    prenom              = forms.CharField(max_length=30,label="Prénom",error_messages=default_errors)
    username            = forms.CharField(max_length=30,label="Nom d'utilisateur",error_messages=default_errors)
    password            = forms.CharField(label="Mot de passe",widget=forms.PasswordInput,error_messages=default_errors)
    confirm_password    = forms.CharField(label="Confirmez votre mot de passe",widget=forms.PasswordInput,error_messages=default_errors)
    email               = forms.EmailField(error_messages=default_errors)
    #birthday            = forms.DateField(widget=forms.widgets.DateInput(format="%d/%m/%Y"),input_formats=["%d/%m/%Y"],label="Date de naissance (jj/mm/aaaa)",error_messages=default_errors)
    telephone           = forms.CharField(max_length=20,label="Numéro de téléphone",error_messages=default_errors)
    adresse             = forms.CharField(max_length=40,error_messages=default_errors)

    def clean_username(self):
        username = self.cleaned_data['username']
        if username:
            if User.objects.filter(username=username):
                raise forms.ValidationError("Utilisateur déja existant")
        return username

    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        if telephone:
            a = re.compile("^[0-9]*$")
            if not a.match(telephone):
                raise forms.ValidationError("Ce champ ne doit contenir que des chiffres")
        return telephone



    def clean(self):
        cleaned_data = super(InscriptionForm, self).clean()  #Vérification par défaut des champs du formulaire
        password            = cleaned_data.get('password')
        confirm_password    = cleaned_data.get('confirm_password')

        if password and confirm_password:   # Si ces deux champs sont valides
            if password != confirm_password:
                #raise forms.ValidationError("Les deux mots de passe ne correspondent pas")
                self._errors["confirm_password"] = self.error_class(["Les deux mots de passe ne correspondent pas"])
                del cleaned_data["confirm_password"]

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur",max_length=30)
    password = forms.CharField(label="Mot de passe",max_length=30,widget=forms.PasswordInput)







