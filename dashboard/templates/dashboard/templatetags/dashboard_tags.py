from django import template

register = template.Library()

@register.filter
def has_perm(user, permission):
    """Check if user has a specific permission"""
    if not hasattr(user, 'role'):
        return False
    
    # Admin role has all permissions
    if user.role.nom.lower() == 'admin':
        return True
    
    # Check if permissions attribute exists
    if not hasattr(user.role, 'permissions') or not user.role.permissions:
        return False
    
    # Convert permissions to list
    permissions_list = [p.strip() for p in user.role.permissions.split(',')]
    
    # Check for permission
    return permission in permissions_list