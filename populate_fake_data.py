import os
import django
from datetime import datetime, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'harmonySchool2.settings')
django.setup()

from dashboard.models import Role, Utilisateur, Categorie, Lieu, Incident, PieceJointe
from django.db import transaction
from django.core.files.base import ContentFile

# First, ensure we have the basic roles
with transaction.atomic():
    # Admin role
    admin_role, _ = Role.objects.get_or_create(
        nom="Admin",
        defaults={
            "permissions": "view_incident,view_own_incident,create_incident,update_incident," +
                          "view_categorie,manage_categorie,view_lieu,manage_lieu," +
                          "view_utilisateur,manage_utilisateur,view_role,manage_role"
        }
    )
    
    # Enseignant role
    enseignant_role, _ = Role.objects.get_or_create(
        nom="Enseignant",
        defaults={
            "permissions": "create_incident,view_incident,update_incident,view_categorie,view_lieu"
        }
    )
    
    # Personnel role
    personnel_role, _ = Role.objects.get_or_create(
        nom="Personnel",
        defaults={
            "permissions": "create_incident,view_incident,view_categorie,view_lieu"
        }
    )
    
    # Etudiant role
    etudiant_role, _ = Role.objects.get_or_create(
        nom="Etudiant",
        defaults={
            "permissions": "create_incident,view_own_incident"
        }
    )

# Create locations
with transaction.atomic():
    locations = [
        {"nom": "Bibliothèque Centrale", "batiment": "A", "etage": "1er", "salle": "A101"},
        {"nom": "Laboratoire Informatique", "batiment": "B", "etage": "2ème", "salle": "B201"},
        {"nom": "Salle de Conférence", "batiment": "C", "etage": "RDC", "salle": "C001"},
        {"nom": "Cafétéria", "batiment": "D", "etage": "RDC", "salle": "D001"},
        {"nom": "Gymnase", "batiment": "E", "etage": "RDC", "salle": "E001"},
        {"nom": "Salle des Professeurs", "batiment": "A", "etage": "2ème", "salle": "A201"}
    ]
    
    for loc_data in locations:
        Lieu.objects.get_or_create(
            nom=loc_data["nom"],
            batiment=loc_data["batiment"],
            etage=loc_data["etage"],
            salle=loc_data["salle"]
        )

# Create categories
with transaction.atomic():
    categories = [
        {"nom": "Infrastructure", "description": "Problèmes liés aux bâtiments, salles, etc."},
        {"nom": "Informatique", "description": "Problèmes informatiques, réseau, etc."},
        {"nom": "Sécurité", "description": "Problèmes de sécurité, accidents, etc."},
        {"nom": "Pédagogie", "description": "Questions pédagogiques, cours, etc."},
        {"nom": "Administrative", "description": "Questions administratives, inscriptions, etc."},
        {"nom": "Maintenance", "description": "Problèmes de maintenance générale"}
    ]
    
    for cat_data in categories:
        Categorie.objects.get_or_create(
            nom=cat_data["nom"],
            defaults={"description": cat_data["description"]}
        )

# Create test users for each role
with transaction.atomic():
    # Admin users
    admin_users = [
        {"email": "admin1@harmonyschool2.com", "nom": "Admin", "prenom": "Principal"},
        {"email": "admin2@harmonyschool2.com", "nom": "Admin", "prenom": "Secondaire"}
    ]
    
    # Enseignant users
    enseignant_users = [
        {"email": "prof1@harmonyschool2.com", "nom": "Dubois", "prenom": "Marie"},
        {"email": "prof2@harmonyschool2.com", "nom": "Martin", "prenom": "Pierre"},
        {"email": "prof3@harmonyschool2.com", "nom": "Leroy", "prenom": "Sophie"}
    ]
    
    # Personnel users
    personnel_users = [
        {"email": "pers1@harmonyschool2.com", "nom": "Petit", "prenom": "Jean"},
        {"email": "pers2@harmonyschool2.com", "nom": "Robert", "prenom": "Claire"}
    ]
    
    # Etudiant users
    etudiant_users = [
        {"email": "etud1@harmonyschool2.com", "nom": "Dupont", "prenom": "Lucas"},
        {"email": "etud2@harmonyschool2.com", "nom": "Moreau", "prenom": "Emma"},
        {"email": "etud3@harmonyschool2.com", "nom": "Lefebvre", "prenom": "Thomas"},
        {"email": "etud4@harmonyschool2.com", "nom": "Garcia", "prenom": "Léa"}
    ]
    
    # Create all users
    for user_data in admin_users:
        Utilisateur.objects.get_or_create(
            email=user_data["email"],
            defaults={
                "nom": user_data["nom"],
                "prenom": user_data["prenom"],
                "role": admin_role,
                "is_staff": True,
                "is_superuser": True
            }
        )
    
    for user_data in enseignant_users:
        Utilisateur.objects.get_or_create(
            email=user_data["email"],
            defaults={
                "nom": user_data["nom"],
                "prenom": user_data["prenom"],
                "role": enseignant_role
            }
        )
    
    for user_data in personnel_users:
        Utilisateur.objects.get_or_create(
            email=user_data["email"],
            defaults={
                "nom": user_data["nom"],
                "prenom": user_data["prenom"],
                "role": personnel_role
            }
        )
    
    for user_data in etudiant_users:
        Utilisateur.objects.get_or_create(
            email=user_data["email"],
            defaults={
                "nom": user_data["nom"],
                "prenom": user_data["prenom"],
                "role": etudiant_role
            }
        )

# Create incidents
with transaction.atomic():
    statuts = ['nouveau', 'en_cours', 'resolu', 'ferme']
    priorites = ['faible', 'moyenne', 'elevee', 'critique']
    
    incident_titles = [
        "Problème de climatisation",
        "Ordinateur en panne",
        "Fuite d'eau",
        "Problème de connexion internet",
        "Lumière défectueuse",
        "Porte bloquée",
        "Problème de son en classe",
        "Tableau interactif ne fonctionne pas",
        "Chauffage défectueux",
        "Problème de sécurité"
    ]
    
    incident_descriptions = [
        "Besoin d'intervention urgente",
        "Problème récurrent",
        "Première occurrence",
        "Situation critique",
        "Problème mineur",
        "Besoin de maintenance préventive",
        "Problème de confort",
        "Impact sur les cours",
        "Problème de sécurité",
        "Besoin de réparation"
    ]
    
    # Get all users, categories, and locations
    all_users = list(Utilisateur.objects.all())
    all_categories = list(Categorie.objects.all())
    all_locations = list(Lieu.objects.all())
    
    # Create 20 random incidents
    for _ in range(20):
        createur = random.choice(all_users)
        assigne = random.choice(all_users)
        categorie = random.choice(all_categories)
        lieu = random.choice(all_locations)
        statut = random.choice(statuts)
        priorite = random.choice(priorites)
        titre = random.choice(incident_titles)
        description = random.choice(incident_descriptions)
        
        # Create incident
        incident = Incident.objects.create(
            titre=titre,
            description=description,
            statut=statut,
            priorite=priorite,
            categorie=categorie,
            createur=createur,
            assigne=assigne,
            lieu=lieu
        )
        
        # Randomly add 0-2 attachments to some incidents
        if random.random() < 0.3:  # 30% chance to have attachments
            for _ in range(random.randint(1, 2)):
                # Create a dummy file content
                file_content = f"This is a test file {random.randint(1, 100)}".encode('utf-8')
                file_name = f"test_file_{random.randint(1, 100)}.txt"
                
                # Create the attachment
                piece_jointe = PieceJointe(
                    nom_fichier=file_name,
                    type="text/plain",
                    taille=len(file_content),
                    incident=incident
                )
                piece_jointe.chemin.save(file_name, ContentFile(file_content), save=True)

print("Database populated successfully with fake data!")
print("\nCreated:")
print("- 4 Roles (Admin, Enseignant, Personnel, Etudiant)")
print("- 6 Locations")
print("- 6 Categories")
print("- 11 Users (2 Admin, 3 Enseignants, 2 Personnel, 4 Etudiants)")
print("- 20 Incidents with random attachments") 