from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff", "date_joined")
    search_fields = ("username", "email")

admin.site.unregister(User)  # Désinscrit l'ancien modèle
admin.site.register(User, UserAdmin)  # Inscrit un modèle personnalisé