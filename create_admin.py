import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'harmonySchool2.settings')
django.setup()

from dashboard.models import Role, Utilisateur

# Create admin role if it doesn't exist
admin_role, created = Role.objects.get_or_create(
    nom="Admin",
    defaults={
        "permissions": "view_incident,view_own_incident,create_incident,update_incident," +
                      "view_categorie,manage_categorie,view_lieu,manage_lieu," +
                      "view_utilisateur,manage_utilisateur,view_role,manage_role"
    }
)

# Create admin user
try:
    admin_user = Utilisateur.objects.get(email="admin@harmonyschool2.com")
    print("Admin user already exists.")
except Utilisateur.DoesNotExist:
    admin_user = Utilisateur.objects.create_user(
        email="admin@harmonyschool2.com",
        nom="Admin",
        prenom="System",
        mot_de_passe="admin123",  # You can change this password
        role=admin_role,
        is_staff=True,
        is_superuser=True
    )
    print("Admin user created successfully!")
    print("Email: admin@harmonyschool2.com")
    print("Password: admin123") 