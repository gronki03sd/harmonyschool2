from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Utilisateur, Role, Categorie, Lieu, Incident, PieceJointe

class LoginForm(AuthenticationForm):
    """Form for user login"""
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Mot de passe'
    }))

class UtilisateurCreationForm(forms.ModelForm):
    """Form for creating a new user"""
    mot_de_passe = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Utilisateur
        fields = ('nom', 'prenom', 'email', 'telephone', 'role')
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }

class RoleForm(forms.ModelForm):
    """Form for creating/editing roles"""
    
    # Define common permissions
    PERMISSION_CHOICES = [
        ('view_incident', 'Voir tous les incidents'),
        ('view_own_incident', 'Voir ses propres incidents'),
        ('create_incident', 'Créer un incident'),
        ('update_incident', 'Modifier un incident'),
        ('view_categorie', 'Voir les catégories'),
        ('manage_categorie', 'Gérer les catégories'),
        ('view_lieu', 'Voir les lieux'),
        ('manage_lieu', 'Gérer les lieux'),
        ('view_utilisateur', 'Voir les utilisateurs'),
        ('manage_utilisateur', 'Gérer les utilisateurs'),
        ('view_role', 'Voir les rôles'),
        ('manage_role', 'Gérer les rôles'),
    ]
    
    # Custom field for permissions (not directly mapped to model)
    permissions_choices = forms.MultipleChoiceField(
        choices=PERMISSION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Permissions'
    )
    
    class Meta:
        model = Role
        fields = ('nom',)
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If editing existing role, set initial values for permissions checkboxes
        if self.instance and self.instance.pk:
            self.fields['permissions_choices'].initial = self.instance.permissions_list
            
    def save(self, commit=True):
        role = super().save(commit=False)
        
        # Save selected permissions as comma-separated string
        selected_permissions = self.cleaned_data.get('permissions_choices', [])
        role.permissions = ','.join(selected_permissions)
        
        if commit:
            role.save()
        return role

class CategorieForm(forms.ModelForm):
    """Form for creating/editing categories"""
    class Meta:
        model = Categorie
        fields = ('nom', 'description')
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class LieuForm(forms.ModelForm):
    """Form for creating/editing locations"""
    class Meta:
        model = Lieu
        fields = ('nom', 'batiment', 'etage', 'salle')
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'batiment': forms.TextInput(attrs={'class': 'form-control'}),
            'etage': forms.TextInput(attrs={'class': 'form-control'}),
            'salle': forms.TextInput(attrs={'class': 'form-control'}),
        }

class IncidentForm(forms.ModelForm):
    """Form for creating/editing incidents"""
    class Meta:
        model = Incident
        fields = ('titre', 'description', 'statut', 'priorite', 'categorie', 'assigne', 'lieu')
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'priorite': forms.Select(attrs={'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'assigne': forms.Select(attrs={'class': 'form-control'}),
            'lieu': forms.Select(attrs={'class': 'form-control'}),
        }

class PieceJointeForm(forms.ModelForm):
    """Form for uploading attachments"""
    class Meta:
        model = PieceJointe
        fields = ('nom_fichier', 'chemin')
        widgets = {
            'nom_fichier': forms.TextInput(attrs={'class': 'form-control'}),
            'chemin': forms.FileInput(attrs={'class': 'form-control'}),
        }

class EditProfileForm(forms.ModelForm):
    """Form for editing user profile"""
    
    class Meta:
        model = Utilisateur
        fields = ('nom', 'prenom', 'email', 'telephone')
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label='Nouveau mot de passe'
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label='Confirmer le mot de passe'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and new_password != confirm_password:
            self.add_error('confirm_password', 'Les mots de passe ne correspondent pas.')
            
        return cleaned_data