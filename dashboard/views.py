from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse
from functools import wraps
from .models import Utilisateur, Role, Categorie, Lieu, Incident, PieceJointe
from .forms import (
    LoginForm, UtilisateurCreationForm, RoleForm, 
    CategorieForm, LieuForm, IncidentForm, PieceJointeForm , EditProfileForm
)
from .decorators import permission_required
from collections import Counter

# ========== Authentication Views ==========

def custom_login(request):
    """View for user login"""
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue, {user.prenom}!')
                return redirect('dashboard_home')
            else:
                messages.error(request, 'Email ou mot de passe incorrect.')
    else:
        form = LoginForm()
    return render(request, 'dashboard/login.html', {'form': form})

@login_required
def custom_logout(request):
    """View for user logout"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('login')

# ========== Dashboard Views ==========

@login_required
def dashboard_home(request):
    """Main dashboard view showing statistics or profile based on role"""
    # Check user role
    role_name = request.user.role.nom.lower()
    
    if role_name == 'admin':
        # Admin gets the full dashboard
        return admin_dashboard(request)
    elif role_name == 'enseignant':
        # Teachers get a modified dashboard
        return enseignant_dashboard(request) 
    elif role_name == 'personnel':
        # Staff get a modified dashboard
        return personnel_dashboard(request)
    else:
        # Students (Etudiant) get the profile view
        return etudiant_dashboard(request)

def admin_dashboard(request):
    """Dashboard view for admin showing all statistics"""
    # Get all incidents
    incidents = Incident.objects.all()

    # Total statistics
    total_incidents = incidents.count()
    incidents_nouveaux = incidents.filter(statut='nouveau').count()
    incidents_en_cours = incidents.filter(statut='en_cours').count()
    incidents_resolus = incidents.filter(statut='resolu').count()

    # Top categories (by name)
    categories = Counter(incident.categorie.nom for incident in incidents if incident.categorie)
    top_categories = categories.most_common(5)

    # Top priorities (by value)
    priorities = Counter(incident.priorite for incident in incidents if incident.priorite)
    top_priorities = priorities.most_common(5)

    # Recent incidents (last 10, adjust as needed)
    incidents_recents = incidents.order_by('-date_creation')[:10]

    context = {
        'total_incidents': total_incidents,
        'incidents_nouveaux': incidents_nouveaux,
        'incidents_en_cours': incidents_en_cours,
        'incidents_resolus': incidents_resolus,
        'top_categories': top_categories,
        'top_priorities': top_priorities,
        'incidents_recents': incidents_recents,
        'user_role': 'admin',
        'is_admin': True
    }
    
    return render(request, 'dashboard/index.html', context)

def enseignant_dashboard(request):
    """Dashboard view for teachers showing all incidents"""
    # Count incidents by status
    total_incidents = Incident.objects.count()
    incidents_nouveaux = Incident.objects.filter(statut='nouveau').count()
    incidents_en_cours = Incident.objects.filter(statut='en_cours').count()
    incidents_resolus = Incident.objects.filter(statut='resolu').count()
    
    # Get incidents by category and priority for charts
    incidents_par_categorie_queryset = Incident.objects.values('categorie__nom').annotate(count=Count('id'))
    incidents_par_priorite_queryset = Incident.objects.values('priorite').annotate(count=Count('id'))
    
    # Convert QuerySet to list for JSON serialization
    incidents_par_categorie = list(incidents_par_categorie_queryset)
    incidents_par_priorite = list(incidents_par_priorite_queryset)
    
    # Get recent incidents
    incidents_recents = Incident.objects.all().order_by('-date_creation')[:5]
    
    # Get user's incidents
    my_incidents = Incident.objects.filter(createur=request.user).order_by('-date_creation')[:5]
    
    context = {
        'total_incidents': total_incidents,
        'incidents_nouveaux': incidents_nouveaux,
        'incidents_en_cours': incidents_en_cours,
        'incidents_resolus': incidents_resolus,
        'incidents_par_categorie': incidents_par_categorie,
        'incidents_par_priorite': incidents_par_priorite,
        'incidents_recents': incidents_recents,
        'my_incidents': my_incidents,
        'user_role': 'enseignant',
        'is_staff': True
    }
    
    return render(request, 'dashboard/staff_dashboard.html', context)

def personnel_dashboard(request):
    """Dashboard view for staff showing all incidents"""
    # Count incidents by status
    total_incidents = Incident.objects.count()
    incidents_nouveaux = Incident.objects.filter(statut='nouveau').count()
    incidents_en_cours = Incident.objects.filter(statut='en_cours').count()
    incidents_resolus = Incident.objects.filter(statut='resolu').count()
    
    # Get incidents by category and priority for charts
    incidents_par_categorie_queryset = Incident.objects.values('categorie__nom').annotate(count=Count('id'))
    incidents_par_priorite_queryset = Incident.objects.values('priorite').annotate(count=Count('id'))
    
    # Convert QuerySet to list for JSON serialization
    incidents_par_categorie = list(incidents_par_categorie_queryset)
    incidents_par_priorite = list(incidents_par_priorite_queryset)
    
    # Get recent incidents
    incidents_recents = Incident.objects.all().order_by('-date_creation')[:5]
    
    # Get user's incidents
    my_incidents = Incident.objects.filter(createur=request.user).order_by('-date_creation')[:5]
    
    context = {
        'total_incidents': total_incidents,
        'incidents_nouveaux': incidents_nouveaux,
        'incidents_en_cours': incidents_en_cours,
        'incidents_resolus': incidents_resolus,
        'incidents_par_categorie': incidents_par_categorie,
        'incidents_par_priorite': incidents_par_priorite,
        'incidents_recents': incidents_recents,
        'my_incidents': my_incidents,
        'user_role': 'personnel',
        'is_staff': True
    }
    
    return render(request, 'dashboard/staff_dashboard.html', context)

def etudiant_dashboard(request):
    """Profile view for student users showing only their incidents"""
    # Get user's incidents counts
    total_incidents = Incident.objects.filter(createur=request.user).count()
    incidents_nouveaux = Incident.objects.filter(createur=request.user, statut='nouveau').count()
    incidents_en_cours = Incident.objects.filter(createur=request.user, statut='en_cours').count()
    incidents_resolus = Incident.objects.filter(createur=request.user, statut='resolu').count()
    
    # Get user's recent incidents
    user_incidents = Incident.objects.filter(createur=request.user).order_by('-date_creation')[:5]
    
    context = {
        'user_incidents': user_incidents,
        'total_incidents': total_incidents,
        'incidents_nouveaux': incidents_nouveaux,
        'incidents_en_cours': incidents_en_cours,
        'incidents_resolus': incidents_resolus,
        'user_role': 'etudiant',
        'is_student': True
    }
    
    return render(request, 'dashboard/student_profile.html', context)

# ========== API Views ==========

@login_required
def get_chart_data(request):
    """API view to provide chart data for dashboard"""
    role_name = request.user.role.nom.lower()
    
    # Pour l'admin, enseignant et personnel, montrer toutes les données
    if role_name in ['admin', 'enseignant', 'personnel']:
        # Get incidents by category
        incidents_par_categorie_queryset = Incident.objects.values('categorie__nom').annotate(count=Count('id'))
        categories_data = list(incidents_par_categorie_queryset)
        
        # Get incidents by priority
        incidents_par_priorite_queryset = Incident.objects.values('priorite').annotate(count=Count('id'))
        priorites_data = list(incidents_par_priorite_queryset)
    else:
        # Pour les étudiants, montrer seulement leurs propres incidents
        # Get incidents by category
        incidents_par_categorie_queryset = Incident.objects.filter(createur=request.user).values('categorie__nom').annotate(count=Count('id'))
        categories_data = list(incidents_par_categorie_queryset)
        
        # Get incidents by priority
        incidents_par_priorite_queryset = Incident.objects.filter(createur=request.user).values('priorite').annotate(count=Count('id'))
        priorites_data = list(incidents_par_priorite_queryset)
    
    # Priority labels translation
    priority_labels = {
        'faible': 'Faible',
        'moyenne': 'Moyenne',
        'elevee': 'Élevée',
        'critique': 'Critique'
    }
    
    # Format data for the charts
    categories = {
        'labels': [item['categorie__nom'] for item in categories_data],
        'counts': [item['count'] for item in categories_data]
    }
    
    priorities = {
        'labels': [priority_labels.get(item['priorite'], item['priorite']) for item in priorites_data],
        'counts': [item['count'] for item in priorites_data],
        'keys': [item['priorite'] for item in priorites_data]
    }
    
    return JsonResponse({
        'categories': categories,
        'priorities': priorities
    })

# ========== User Management Views ==========

@login_required
@permission_required('view_utilisateur')
def liste_utilisateurs(request):
    """View to list all users - requires view_utilisateur permission"""
    utilisateurs = Utilisateur.objects.all()
    return render(request, 'dashboard/utilisateurs/liste.html', {'utilisateurs': utilisateurs})

@login_required
@permission_required('manage_utilisateur')
def creer_utilisateur(request):
    """View to create a new user - requires manage_utilisateur permission"""
    if request.method == 'POST':
        form = UtilisateurCreationForm(request.POST)
        if form.is_valid():
            utilisateur = form.save(commit=False)
            mot_de_passe = form.cleaned_data.get('mot_de_passe')
            utilisateur.set_password(mot_de_passe)
            utilisateur.actif = request.POST.get('actif') == 'on'
            utilisateur.save()
            messages.success(request, 'Utilisateur créé avec succès!')
            return redirect('liste_utilisateurs')
        else:
            messages.error(request, 'Erreur lors de la création de l\'utilisateur.')
    else:
        form = UtilisateurCreationForm()
    
    return render(request, 'dashboard/utilisateurs/creer.html', {'form': form})

@login_required
@permission_required('manage_utilisateur')
def modifier_utilisateur(request, pk):
    """View to edit a user - requires manage_utilisateur permission"""
    utilisateur = get_object_or_404(Utilisateur, pk=pk)
    
    if request.method == 'POST':
        form = UtilisateurCreationForm(request.POST, instance=utilisateur)
        if form.is_valid():
            utilisateur = form.save(commit=False)
            
            # Update password if provided
            mot_de_passe = request.POST.get('mot_de_passe')
            if mot_de_passe:
                utilisateur.set_password(mot_de_passe)
            
            # Update active status
            utilisateur.actif = request.POST.get('actif') == 'on'
            
            utilisateur.save()
            messages.success(request, 'Utilisateur modifié avec succès!')
            return redirect('liste_utilisateurs')
        else:
            messages.error(request, 'Erreur lors de la modification de l\'utilisateur.')
    else:
        form = UtilisateurCreationForm(instance=utilisateur)
    
    return render(request, 'dashboard/utilisateurs/modifier.html', {
        'form': form,
        'utilisateur': utilisateur
    })

@login_required
@permission_required('manage_utilisateur')
def supprimer_utilisateur(request, pk):
    """View to delete a user - requires manage_utilisateur permission"""
    utilisateur = get_object_or_404(Utilisateur, pk=pk)
    
    if request.method == 'POST':
        utilisateur.delete()
        messages.success(request, 'Utilisateur supprimé avec succès!')
        return redirect('liste_utilisateurs')
    
    return render(request, 'dashboard/utilisateurs/supprimer.html', {'utilisateur': utilisateur})

# ========== Role Management Views ==========

@login_required
@permission_required('view_role')
def liste_roles(request):
    """View to list all roles - requires view_role permission"""
    roles = Role.objects.all()
    return render(request, 'dashboard/roles/liste.html', {'roles': roles})

@login_required
@permission_required('manage_role')
def creer_role(request):
    """View to create a new role - requires manage_role permission"""
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rôle créé avec succès!')
            return redirect('liste_roles')
        else:
            messages.error(request, 'Erreur lors de la création du rôle.')
    else:
        form = RoleForm()
    
    return render(request, 'dashboard/roles/creer.html', {'form': form})

@login_required
@permission_required('manage_role')
def modifier_role(request, pk):
    """View to edit a role - requires manage_role permission"""
    role = get_object_or_404(Role, pk=pk)
    
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rôle modifié avec succès!')
            return redirect('liste_roles')
        else:
            messages.error(request, 'Erreur lors de la modification du rôle.')
    else:
        form = RoleForm(instance=role)
    
    return render(request, 'dashboard/roles/modifier.html', {
        'form': form,
        'role': role
    })

@login_required
@permission_required('manage_role')
def supprimer_role(request, pk):
    """View to delete a role - requires manage_role permission"""
    role = get_object_or_404(Role, pk=pk)
    users_with_role = role.utilisateur_set.count()
    
    if request.method == 'POST':
        if role.utilisateur_set.exists():
            messages.error(request, 'Ce rôle ne peut pas être supprimé car il est attribué à des utilisateurs.')
            return redirect('liste_roles')
        
        role.delete()
        messages.success(request, 'Rôle supprimé avec succès!')
        return redirect('liste_roles')
    
    return render(request, 'dashboard/roles/supprimer.html', {
        'role': role,
        'users_with_role': users_with_role
    })

# ========== Category Management Views ==========

@login_required
@permission_required('view_categorie')
def liste_categories(request):
    """View to list all categories - requires view_categorie permission"""
    categories = Categorie.objects.all()
    return render(request, 'dashboard/categories/liste.html', {'categories': categories})

@login_required
@permission_required('manage_categorie')
def creer_categorie(request):
    """View to create a new category - requires manage_categorie permission"""
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catégorie créée avec succès!')
            return redirect('liste_categories')
        else:
            messages.error(request, 'Erreur lors de la création de la catégorie.')
    else:
        form = CategorieForm()
    
    return render(request, 'dashboard/categories/creer.html', {'form': form})

@login_required
@permission_required('manage_categorie')
def modifier_categorie(request, pk):
    """View to edit a category - requires manage_categorie permission"""
    categorie = get_object_or_404(Categorie, pk=pk)
    
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catégorie modifiée avec succès!')
            return redirect('liste_categories')
        else:
            messages.error(request, 'Erreur lors de la modification de la catégorie.')
    else:
        form = CategorieForm(instance=categorie)
    
    return render(request, 'dashboard/categories/modifier.html', {
        'form': form,
        'categorie': categorie
    })

@login_required
@permission_required('manage_categorie')
def supprimer_categorie(request, pk):
    """View to delete a category - requires manage_categorie permission"""
    categorie = get_object_or_404(Categorie, pk=pk)
    
    if request.method == 'POST':
        if categorie.incident_set.exists():
            messages.warning(request, 'Cette catégorie est utilisée par des incidents. Tous les incidents associés seront également supprimés.')
        
        categorie.delete()
        messages.success(request, 'Catégorie supprimée avec succès!')
        return redirect('liste_categories')
    
    return render(request, 'dashboard/categories/supprimer.html', {'categorie': categorie})

# ========== Location Management Views ==========

@login_required
@permission_required('view_lieu')
def liste_lieux(request):
    """View to list all locations - requires view_lieu permission"""
    lieux = Lieu.objects.all()
    return render(request, 'dashboard/lieux/liste.html', {'lieux': lieux})

@login_required
@permission_required('manage_lieu')
def creer_lieu(request):
    """View to create a new location - requires manage_lieu permission"""
    if request.method == 'POST':
        form = LieuForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lieu créé avec succès!')
            return redirect('liste_lieux')
        else:
            messages.error(request, 'Erreur lors de la création du lieu.')
    else:
        form = LieuForm()
    
    return render(request, 'dashboard/lieux/creer.html', {'form': form})

@login_required
@permission_required('manage_lieu')
def modifier_lieu(request, pk):
    """View to edit a location - requires manage_lieu permission"""
    lieu = get_object_or_404(Lieu, pk=pk)
    
    if request.method == 'POST':
        form = LieuForm(request.POST, instance=lieu)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lieu modifié avec succès!')
            return redirect('liste_lieux')
        else:
            messages.error(request, 'Erreur lors de la modification du lieu.')
    else:
        form = LieuForm(instance=lieu)
    
    return render(request, 'dashboard/lieux/modifier.html', {
        'form': form,
        'lieu': lieu
    })

@login_required
@permission_required('manage_lieu')
def supprimer_lieu(request, pk):
    """View to delete a location - requires manage_lieu permission"""
    lieu = get_object_or_404(Lieu, pk=pk)
    
    if request.method == 'POST':
        if lieu.incident_set.exists():
            messages.warning(request, 'Ce lieu est utilisé par des incidents. Les incidents associés seront mis à jour pour ne plus référencer ce lieu.')
            # Update incidents to remove this location
            for incident in lieu.incident_set.all():
                incident.lieu = None
                incident.save()
        
        lieu.delete()
        messages.success(request, 'Lieu supprimé avec succès!')
        return redirect('liste_lieux')
    
    return render(request, 'dashboard/lieux/supprimer.html', {'lieu': lieu})

# ========== Incident Management Views ==========

@login_required
def liste_incidents(request):
    """View to list incidents based on user role"""
    role_name = request.user.role.nom.lower()
    
    if role_name == 'admin' or 'view_incident' in request.user.role.permissions_list:
        # Admin, teachers and staff see all incidents
        incidents = Incident.objects.all().order_by('-date_creation')
    else:
        # Students only see their own incidents
        incidents = Incident.objects.filter(createur=request.user).order_by('-date_creation')
    
    return render(request, 'dashboard/incidents/liste.html', {'incidents': incidents})

@login_required
def creer_incident(request):
    """View to create a new incident - All roles can access"""
    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.createur = request.user
            incident.save()
            
            # Handle uploaded files
            files = request.FILES.getlist('pieces_jointes')
            for f in files:
                PieceJointe.objects.create(
                    nom_fichier=f.name,
                    type=f.content_type,
                    taille=f.size,
                    chemin=f,
                    incident=incident
                )
            
            messages.success(request, 'Incident créé avec succès!')
            return redirect('detail_incident', pk=incident.pk)
        else:
            messages.error(request, 'Erreur lors de la création de l\'incident.')
    else:
        form = IncidentForm()
    
    return render(request, 'dashboard/incidents/creer.html', {'form': form})

@login_required
def detail_incident(request, pk):
    """View to see incident details"""
    incident = get_object_or_404(Incident, pk=pk)
    
    # Check if user has permission to view
    role_name = request.user.role.nom.lower()
    if role_name != 'admin' and 'view_incident' not in request.user.role.permissions_list and incident.createur != request.user:
        messages.error(request, "Vous n'avez pas la permission de voir cet incident.")
        return redirect('liste_incidents')
    
    pieces_jointes = incident.pieces_jointes.all()
    
    return render(request, 'dashboard/incidents/detail.html', {
        'incident': incident,
        'pieces_jointes': pieces_jointes
    })

@login_required
def modifier_incident(request, pk):
    """View to edit an incident"""
    incident = get_object_or_404(Incident, pk=pk)
    
    # Check if user has permission to edit
    role_name = request.user.role.nom.lower()
    if role_name != 'admin' and 'update_incident' not in request.user.role.permissions_list and incident.createur != request.user:
        messages.error(request, "Vous n'avez pas la permission de modifier cet incident.")
        return redirect('liste_incidents')
    
    pieces_jointes = incident.pieces_jointes.all()
    
    if request.method == 'POST':
        form = IncidentForm(request.POST, instance=incident)
        if form.is_valid():
            updated_incident = form.save()
            
            # Handle uploaded files
            files = request.FILES.getlist('pieces_jointes')
            for f in files:
                PieceJointe.objects.create(
                    nom_fichier=f.name,
                    type=f.content_type,
                    taille=f.size,
                    chemin=f,
                    incident=updated_incident
                )
            
            messages.success(request, 'Incident modifié avec succès!')
            return redirect('detail_incident', pk=updated_incident.pk)
        else:
            messages.error(request, 'Erreur lors de la modification de l\'incident.')
    else:
        form = IncidentForm(instance=incident)
    
    return render(request, 'dashboard/incidents/modifier.html', {
        'form': form,
        'incident': incident,
        'pieces_jointes': pieces_jointes
    })

@login_required
@permission_required('update_incident')
def supprimer_incident(request, pk):
    """View to delete an incident - requires update_incident permission"""
    incident = get_object_or_404(Incident, pk=pk)
    
    # If not admin, check if user is the creator
    role_name = request.user.role.nom.lower()
    if role_name != 'admin' and incident.createur != request.user:
        messages.error(request, "Vous n'avez pas la permission de supprimer cet incident.")
        return redirect('liste_incidents')
    
    if request.method == 'POST':
        incident.delete()
        messages.success(request, 'Incident supprimé avec succès!')
        return redirect('liste_incidents')
    
    return render(request, 'dashboard/incidents/supprimer.html', {'incident': incident})

@login_required
def supprimer_piece_jointe(request, pk):
    """View to delete an attachment"""
    piece_jointe = get_object_or_404(PieceJointe, pk=pk)
    incident_id = piece_jointe.incident.id
    incident = piece_jointe.incident
    
    # Check if user has permission to delete
    role_name = request.user.role.nom.lower()
    if role_name != 'admin' and 'update_incident' not in request.user.role.permissions_list and incident.createur != request.user:
        messages.error(request, "Vous n'avez pas la permission de supprimer cette pièce jointe.")
        return redirect('detail_incident', pk=incident_id)
    
    if request.method == 'POST':
        piece_jointe.delete()
        messages.success(request, 'Pièce jointe supprimée avec succès!')
        return redirect('detail_incident', pk=incident_id)
    
    return render(request, 'dashboard/pieces_jointes/supprimer.html', {
        'piece_jointe': piece_jointe,
        'incident': incident
    })

# ========== User Profile View ==========

@login_required
def profile(request):
    """View for user's profile showing their information"""
    user = request.user
    
    # Get user's incidents counts
    total_incidents = Incident.objects.filter(createur=user).count()
    incidents_nouveaux = Incident.objects.filter(createur=user, statut='nouveau').count()
    incidents_en_cours = Incident.objects.filter(createur=user, statut='en_cours').count()
    incidents_resolus = Incident.objects.filter(createur=user, statut='resolu').count()
    
    # Get user's recent incidents
    user_incidents = Incident.objects.filter(createur=user).order_by('-date_creation')[:5]
    
    context = {
        'user': user,
        'user_incidents': user_incidents,
        'total_incidents': total_incidents,
        'incidents_nouveaux': incidents_nouveaux,
        'incidents_en_cours': incidents_en_cours,
        'incidents_resolus': incidents_resolus,
    }
    
    return render(request, 'dashboard/profile/view.html', context)

@login_required
def edit_profile(request):
    """View for editing user's profile"""
    user = request.user
    
    if request.method == 'POST':
        # Handle form submission
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            
            # Update password if provided
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                user.set_password(new_password)
                user.save()
                # Re-authenticate user to prevent logout after password change
                login(request, authenticate(username=user.email, password=new_password))
                
            messages.success(request, 'Profil mis à jour avec succès!')
            return redirect('profile')
        else:
            messages.error(request, 'Erreur lors de la mise à jour du profil.')
    else:
        # Display form
        form = EditProfileForm(instance=user)
    
    return render(request, 'dashboard/profile/edit.html', {
        'form': form, 
        'user': user
    })