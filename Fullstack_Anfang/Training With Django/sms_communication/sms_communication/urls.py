from django.contrib import admin
from django.urls import path, include
from messagerie import views  # Importer les vues de ton application messagerie

urlpatterns = [
    # Page d'administration
    path('admin/', admin.site.urls),
    
    # Inclure les URLs de l'application messagerie
    path('messagerie/', include('messagerie.urls')),
    
    # Page d'accueil pour les utilisateurs non connectés (redirige vers l'inscription)
    path('', views.home_public, name='home'),
]
