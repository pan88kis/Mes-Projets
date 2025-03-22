from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Message
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.db.models import Q  # Pour les requêtes OR

def test_template(request):
    return render(request, 'messagerie/test.html')

@login_required
def home(request):
    # Rediriger directement vers la boîte de réception (inbox) de l'utilisateur connecté
    return redirect('inbox')

def home_public(request):
    if request.user.is_authenticated:
        return redirect('inbox')  # Si l'utilisateur est connecté, rediriger vers la boîte de réception
    return render(request, 'messagerie/home_public.html')  # Si non connecté, afficher la page publique


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Sauvegarde l'utilisateur
            login(request, user)  # Connecte l'utilisateur automatiquement
            return redirect("home")  # Redirige après inscription
        else:
            print("Formulaire invalide", form.errors)  # Affiche les erreurs dans la console
    else:
        form = RegisterForm()

    return render(request, "messagerie/register.html", {"form": form})

def envoyer_message(request, receiver_id):
    receiver = User.objects.get(id=receiver_id)  # Récupérer le destinataire
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=request.user))
    ).order_by('-created_at')  # Récupérer les messages échangés entre les deux utilisateurs

    if request.method == 'POST':
        content = request.POST.get('content')
        message = Message(sender=request.user, receiver=receiver, content=content)
        message.save()
        return redirect('envoyer_message', receiver_id=receiver.id)

    return render(request, 'messagerie/envoyer_message.html', {'messages': messages, 'receiver': receiver})


def inbox(request):
    # Récupérer les messages reçus
    messages_reçus = Message.objects.filter(receiver=request.user).order_by('-created_at')

    # Récupérer la valeur de recherche de l'URL (si présente)
    search_query = request.GET.get('search', '')

    # Si une valeur de recherche est présente, filtrer les utilisateurs par nom d'utilisateur
    if search_query:
        users = User.objects.filter(username__icontains=search_query).exclude(id=request.user.id)  # Ignorer l'utilisateur connecté
    else:
        users = []  # Si aucune recherche n'est faite, ne rien afficher

    return render(request, 'messagerie/inbox.html', {
        'messages_reçus': messages_reçus,
        'users': users,  # Utilisateurs correspondant à la recherche
        'search_query': search_query,  # La recherche effectuée
    })

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'messagerie/login.html', {'form': form})

def logout_view(request):
    logout(request)  # Déconnecte l'utilisateur
    return redirect('home')  # Redirige vers la page d'accueil publique