# dashboard/decorators.py
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def permission_required(permission):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Check if user is authenticated
            if not request.user.is_authenticated:
                return redirect('custom_login')
                
            # Check if user has role attribute
            if not hasattr(request.user, 'role'):
                messages.error(request, "Vous n'avez pas de rôle défini.")
                return redirect('dashboard_home')
                
            # Admin bypasses permission checks - la vérification est insensible à la casse
            if request.user.role.nom.lower() == 'admin':
                return view_func(request, *args, **kwargs)
                
            # Check if role has permissions attribute
            if not hasattr(request.user.role, 'permissions'):
                messages.error(request, "Votre rôle n'a pas de permissions définies.")
                return redirect('dashboard_home')
                
            # Get permissions list
            permissions_list = []
            if request.user.role.permissions:
                permissions_list = [p.strip() for p in request.user.role.permissions.split(',')]
                
            # Check permission
            if permission not in permissions_list:
                messages.error(request, "Vous n'avez pas la permission d'accéder à cette page.")
                return redirect('dashboard_home')
                
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def role_required(allowed_roles):
    """Decorator that checks if user has one of the allowed roles"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('custom_login')
                
            if not hasattr(request.user, 'role'):
                messages.error(request, "Votre compte n'a pas de rôle attribué.")
                return redirect('dashboard_home')
                
            # Vérification insensible à la casse
            if request.user.role.nom.lower() not in [role.lower() for role in allowed_roles]:
                messages.error(request, "Vous n'avez pas la permission d'accéder à cette page.")
                return redirect('dashboard_home')
                
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator