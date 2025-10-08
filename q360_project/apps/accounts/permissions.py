"""
Custom permissions for accounts app.
"""
from rest_framework import permissions


class IsSuperAdminOrAdmin(permissions.BasePermission):
    """
    Permission class that allows access only to superadmin or admin users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin()


class IsSuperAdmin(permissions.BasePermission):
    """
    Permission class that allows access only to superadmin users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superadmin()


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission class that allows access to object owner or admin users.
    """

    def has_object_permission(self, request, view, obj):
        # Admin can access any object
        if request.user.is_admin():
            return True

        # Check if user is the owner
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user


class IsManagerOrAbove(permissions.BasePermission):
    """
    Permission class that allows access to manager level and above.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_manager()
