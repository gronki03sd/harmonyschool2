import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'harmonySchool2.settings')
django.setup()

from dashboard.models import Utilisateur

# Reset admin password
try:
    admin_user = Utilisateur.objects.get(email="admin@harmonyschool2.com")
    admin_user.set_password("admin123")
    admin_user.save()
    print("Admin password has been reset successfully!")
    print("Email: admin@harmonyschool2.com")
    print("New Password: admin123")
except Utilisateur.DoesNotExist:
    print("Admin user not found!") 