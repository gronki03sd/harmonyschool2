# dashboard/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    
    # Utilisateurs
    path('utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('utilisateurs/creer/', views.creer_utilisateur, name='creer_utilisateur'),
    path('utilisateurs/modifier/<int:pk>/', views.modifier_utilisateur, name='modifier_utilisateur'),
    path('utilisateurs/supprimer/<int:pk>/', views.supprimer_utilisateur, name='supprimer_utilisateur'),
    
    # Roles
    path('roles/', views.liste_roles, name='liste_roles'),
    path('roles/creer/', views.creer_role, name='creer_role'),
    path('roles/modifier/<int:pk>/', views.modifier_role, name='modifier_role'),
    path('roles/supprimer/<int:pk>/', views.supprimer_role, name='supprimer_role'),
    
    # Categories
    path('categories/', views.liste_categories, name='liste_categories'),
    path('categories/creer/', views.creer_categorie, name='creer_categorie'),
    path('categories/modifier/<int:pk>/', views.modifier_categorie, name='modifier_categorie'),
    path('categories/supprimer/<int:pk>/', views.supprimer_categorie, name='supprimer_categorie'),
    
    # Lieux
    path('lieux/', views.liste_lieux, name='liste_lieux'),
    path('lieux/creer/', views.creer_lieu, name='creer_lieu'),
    path('lieux/modifier/<int:pk>/', views.modifier_lieu, name='modifier_lieu'),
    path('lieux/supprimer/<int:pk>/', views.supprimer_lieu, name='supprimer_lieu'),
    
    # Incidents
    path('incidents/', views.liste_incidents, name='liste_incidents'),
    path('incidents/creer/', views.creer_incident, name='creer_incident'),
    path('incidents/<int:pk>/', views.detail_incident, name='detail_incident'),
    path('incidents/modifier/<int:pk>/', views.modifier_incident, name='modifier_incident'),
    path('incidents/supprimer/<int:pk>/', views.supprimer_incident, name='supprimer_incident'),
    
    # Pieces jointes
    path('pieces-jointes/supprimer/<int:pk>/', views.supprimer_piece_jointe, name='supprimer_piece_jointe'),
    path('api/chart-data/', views.get_chart_data, name='get_chart_data'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
   
]