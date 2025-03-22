from django.urls import path
from . import views

urlpatterns = [
    # Page d'accueil
    path('', views.home_public, name='home'),  

    # Page d'inscription
    path('register/', views.register, name='register'),
    
    # Page de connexion (login)
    path('login/', views.login_view, name='login'),
    
    # Inbox de l'utilisateur (messages reçus)
    path('inbox/', views.inbox, name='inbox'),
    
    # Envoi de message (avec l'ID du destinataire)
    path('envoyer_message/<int:receiver_id>/', views.envoyer_message, name='envoyer_message'),
    
    # Route pour la déconnexion
    path('logout/', views.logout_view, name='logout'),  
]
