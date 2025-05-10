# Place this file in the root directory of your project
# Run it with: python manage.py shell < init_data.py

from dashboard.models import Role, Utilisateur, Categorie, Lieu
from django.db import transaction

# Create default roles
with transaction.atomic():
    # Admin role
    admin_role, created = Role.objects.get_or_create(
        nom="Admin",
        defaults={"permissions": "all"}
    )
    
    # Teacher role
    enseignant_role, created = Role.objects.get_or_create(
        nom="Enseignant",
        defaults={"permissions": "create_incident,view_incident,update_incident"}
    )
    
    # Staff role
    personnel_role, created = Role.objects.get_or_create(
        nom="Personnel",
        defaults={"permissions": "create_incident,view_incident"}
    )
    
    # Student role
    etudiant_role, created = Role.objects.get_or_create(
        nom="Etudiant",
        defaults={"permissions": "create_incident,view_own_incident"}
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

print("Initial data setup complete.")