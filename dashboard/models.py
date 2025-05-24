from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class RoleManager(BaseUserManager):
    def create_role(self, nom, permissions):
        role = self.model(nom=nom, permissions=permissions)
        role.save(using=self._db)
        return role

class Role(models.Model):
    nom = models.CharField(max_length=30, unique=True)
    permissions = models.TextField(blank=True)
    
    @property
    def permissions_list(self):
        """Convert comma-separated permissions string to a list"""
        if not self.permissions:
            return []
        return [p.strip() for p in self.permissions.split(',')]
    
    def has_permission(self, permission):
        """Check if role has a specific permission"""
        # Admin role has all permissions - vérification insensible à la casse
        if self.nom.lower() == 'admin':
            return True
        return permission in self.permissions_list
    
    def __str__(self):
        return self.nom

class UtilisateurManager(BaseUserManager):
    def create_user(self, email, nom, prenom, mot_de_passe=None, **extra_fields):
        if not email:
            raise ValueError('Email est obligatoire')
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            nom=nom,
            prenom=prenom,
            **extra_fields
        )
        user.set_password(mot_de_passe)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, nom, prenom, mot_de_passe=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('actif', True)
        
        # Get or create admin role
        from django.apps import apps
        Role = apps.get_model('dashboard', 'Role')
        admin_role, created = Role.objects.get_or_create(
            nom='Admin',
            defaults={
                'permissions': "view_incident,view_own_incident,create_incident,update_incident," +
                              "view_categorie,manage_categorie,view_lieu,manage_lieu," +
                              "view_utilisateur,manage_utilisateur,view_role,manage_role"
            }
        )
        extra_fields.setdefault('role', admin_role)
        
        return self.create_user(email, nom, prenom, mot_de_passe, **extra_fields)

class Utilisateur(AbstractBaseUser, PermissionsMixin):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    actif = models.BooleanField(default=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    
    # Required for Django's admin
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UtilisateurManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    @property
    def is_active(self):
        return self.actif

class Categorie(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nom

class Lieu(models.Model):
    nom = models.CharField(max_length=50)
    batiment = models.CharField(max_length=50, blank=True, null=True)
    etage = models.CharField(max_length=20, blank=True, null=True)
    salle = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        parts = [self.nom]
        if self.batiment:
            parts.append(self.batiment)
        if self.salle:
            parts.append(self.salle)
        return " - ".join(parts)

class Incident(models.Model):
    STATUT_CHOICES = [
        ('nouveau', 'Nouveau'),
        ('en_cours', 'En cours'),
        ('resolu', 'Résolu'),
        ('ferme', 'Fermé'),
    ]
    
    PRIORITE_CHOICES = [
        ('faible', 'Faible'),
        ('moyenne', 'Moyenne'),
        ('elevee', 'Élevée'),
        ('critique', 'Critique'),
    ]
    
    titre = models.CharField(max_length=100)
    description = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='nouveau')
    priorite = models.CharField(max_length=10, choices=PRIORITE_CHOICES, default='moyenne')
    categorie = models.ForeignKey('Categorie', on_delete=models.CASCADE)
    createur = models.ForeignKey('Utilisateur', related_name='incidents_crees', on_delete=models.CASCADE)
    assigne = models.ForeignKey('Utilisateur', related_name='incidents_assignes', on_delete=models.CASCADE, blank=True, null=True)
    lieu = models.ForeignKey('Lieu', on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.titre
    
    def get_statut_display(self):
        return dict(self.STATUT_CHOICES).get(self.statut, self.statut)
    
    def get_priorite_display(self):
        return dict(self.PRIORITE_CHOICES).get(self.priorite, self.priorite)

class PieceJointe(models.Model):
    nom_fichier = models.CharField(max_length=255)
    type = models.CharField(max_length=50, blank=True, null=True)
    taille = models.IntegerField(blank=True, null=True)
    chemin = models.FileField(upload_to='pieces_jointes/')
    incident = models.ForeignKey('Incident', on_delete=models.CASCADE, related_name='pieces_jointes')
    
    def __str__(self):
        return self.nom_fichier