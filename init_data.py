# Place this file in the root directory of your project
# Run it with: python manage.py shell < init_data.py

from dashboard.models import Role, Utilisateur, Categorie, Lieu
from django.db import transaction

# Create default roles
with transaction.atomic():
    # Admin role with all permissions
    admin_role, created = Role.objects.get_or_create(
        nom="Admin",
        defaults={
            "permissions": "view_incident,view_own_incident,create_incident,update_incident," +
                           "view_categorie,manage_categorie,view_lieu,manage_lieu," +
                           "view_utilisateur,manage_utilisateur,view_role,manage_role"
        }
    )
    if not created:
        # Si le rôle existe déjà, on met à jour ses permissions
        admin_role.permissions = "view_incident,view_own_incident,create_incident,update_incident," + \
                               "view_categorie,manage_categorie,view_lieu,manage_lieu," + \
                               "view_utilisateur,manage_utilisateur,view_role,manage_role"
        admin_role.save()
    
    # Teacher role
    enseignant_role, created = Role.objects.get_or_create(
        nom="Enseignant",
        defaults={
            "permissions": "create_incident,view_incident,update_incident,view_categorie,view_lieu"
        }
    )
    
    # Staff role
    personnel_role, created = Role.objects.get_or_create(
        nom="Personnel",
        defaults={
            "permissions": "create_incident,view_incident,view_categorie,view_lieu"
        }
    )
    
    # Student role
    etudiant_role, created = Role.objects.get_or_create(
        nom="Etudiant",
        defaults={
            "permissions": "create_incident,view_own_incident"
        }
    )
    
    print("Default roles created.")

# Create admin user if it doesn't exist
try:
    admin_user = Utilisateur.objects.get(email="admin@harmonyschool2.com")
    print("Admin user already exists.")
except Utilisateur.DoesNotExist:
    admin_user = Utilisateur.objects.create_user(
        email="admin@harmonyschool2.com",
        nom="Admin",
        prenom="System",
        mot_de_passe="admin123",  # Change this in production!
        role=admin_role,
        is_staff=True,
        is_superuser=True
    )
    print("Admin user created.")

# Create default categories
with transaction.atomic():
    default_categories = [
        {"nom": "Infrastructure", "description": "Problèmes liés aux bâtiments, salles, etc."},
        {"nom": "Informatique", "description": "Problèmes informatiques, réseau, etc."},
        {"nom": "Sécurité", "description": "Problèmes de sécurité, accidents, etc."},
        {"nom": "Pédagogie", "description": "Questions pédagogiques, cours, etc."},
        {"nom": "Administrative", "description": "Questions administratives, inscriptions, etc."},
    ]
    
    for cat_data in default_categories:
        Categorie.objects.get_or_create(
            nom=cat_data["nom"],
            defaults={"description": cat_data["description"]}
        )
    
    print("Default categories created.")

# Create default locations
with transaction.atomic():
    default_locations = [
        {"nom": "Bâtiment Principal", "batiment": "A", "etage": "RDC", "salle": "Hall"},
        {"nom": "Bibliothèque", "batiment": "B", "etage": "1er", "salle": "B101"},
        {"nom": "Gymnase", "batiment": "C", "etage": "RDC", "salle": "G001"},
        {"nom": "Laboratoire", "batiment": "A", "etage": "2ème", "salle": "A201"},
        {"nom": "Salle Informatique", "batiment": "B", "etage": "2ème", "salle": "B205"},
    ]
    
    for loc_data in default_locations:
        Lieu.objects.get_or_create(
            nom=loc_data["nom"],
            batiment=loc_data["batiment"],
            etage=loc_data["etage"],
            salle=loc_data["salle"]
        )
    
    print("Default locations created.")

# Ajouter des utilisateurs de test pour chaque rôle
with transaction.atomic():
    # Enseignant
    try:
        enseignant = Utilisateur.objects.get(email="enseignant@harmonyschool2.com")
        print("Teacher user already exists.")
    except Utilisateur.DoesNotExist:
        enseignant = Utilisateur.objects.create_user(
            email="enseignant@harmonyschool2.com",
            nom="Dupont",
            prenom="Marie",
            mot_de_passe="password123",
            role=enseignant_role
        )
        print("Teacher user created.")
    
    # Personnel
    try:
        personnel = Utilisateur.objects.get(email="personnel@harmonyschool2.com")
        print("Staff user already exists.")
    except Utilisateur.DoesNotExist:
        personnel = Utilisateur.objects.create_user(
            email="personnel@harmonyschool2.com",
            nom="Martin",
            prenom="Pierre",
            mot_de_passe="password123",
            role=personnel_role
        )
        print("Staff user created.")
    
    # Étudiant
    try:
        etudiant = Utilisateur.objects.get(email="etudiant@harmonyschool2.com")
        print("Student user already exists.")
    except Utilisateur.DoesNotExist:
        etudiant = Utilisateur.objects.create_user(
            email="etudiant@harmonyschool2.com",
            nom="Petit",
            prenom="Julie",
            mot_de_passe="password123",
            role=etudiant_role
        )
        print("Student user created.")

print("Initial data setup complete.")