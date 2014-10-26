from membre.forms import InscriptionForm
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render, get_object_or_404
from membre.forms import InscriptionForm, LoginForm
from django.contrib.auth.models import User
from membre.models import Membre
from django.contrib.auth import authenticate, login, logout
from panier.models import Panier
from django.contrib.auth.decorators import login_required


def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST) #Nous reprenons les donnees
        if form.is_valid():
            nom              = form.cleaned_data['nom']
            prenom           = form.cleaned_data['prenom']
            username         = form.cleaned_data['username']
            password         = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            email            = form.cleaned_data['email']
            #birthday         = form.cleaned_data['birthday']
            telephone        = form.cleaned_data['telephone']
            adresse          = form.cleaned_data['adresse']

            user = User(username=username,email=email)
            user.set_password(password)
            user.first_name = prenom
            user.last_name = nom
            user.save()
            membre = Membre(user=user, adress=adresse, phone_number=telephone)
            membre.save()
            panier = Panier(user=user)
            panier.save()

            return render(request,'index.html')
            #membre = Membre(pseudo=pseudo,password=password,nom=nom,prenom=prenom,email=email,adresse=adresse,num_tel=num_tel)
            #membre.save()

    else:
        form = InscriptionForm()
    return render(request,'membre/inscription.html',locals())


def connexion(request):
    error = False

    if request.method == "POST":
        form = LoginForm(request.POST)
        if(form.is_valid()):
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user:
                login(request,user)
                return redirect('/')
            else:
                error = True
    else:
        form = LoginForm()
    return render(request,'membre/login.html',locals())

@login_required
def deconnexion(request):
    logout(request)
    return redirect('/')

@login_required
def modifier_profil(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST) #Nous reprenons les donnees
        if form.is_valid():
            nom              = form.cleaned_data['nom']
            prenom           = form.cleaned_data['prenom']
            username         = form.cleaned_data['username']
            password         = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            email            = form.cleaned_data['email']
            #birthday         = form.cleaned_data['birthday']
            telephone        = form.cleaned_data['telephone']
            adresse          = form.cleaned_data['adresse']
            user = request.user
            user.username = username
            user.email = email
            user.set_password(password)
            user.first_name = prenom
            user.last_name = nom
            user.save()
            membre = user.membre
            membre.adress = adresse
            membre.phone_number = telephone
            membre.save()

            return render(request,'index.html')
            #membre = Membre(pseudo=pseudo,password=password,nom=nom,prenom=prenom,email=email,adresse=adresse,num_tel=num_tel)
            #membre.save()

    else:
        utilisateur = request.user
        form = InscriptionForm(initial={'nom':utilisateur.first_name, 'prenom':utilisateur.last_name, 'username':utilisateur.username, 'email':utilisateur.email, 'telephone':utilisateur.membre.phone_number,'adresse':utilisateur.membre.adress})
    return render(request,'membre/profil.html',locals())


