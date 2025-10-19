"""
Row-level access helpers and permission utilities.
"""
from __future__ import annotations

from typing import Iterable

from django.db.models import Q, QuerySet
from rest_framework.permissions import BasePermission

from .rbac import RoleManager


def filter_queryset_for_user(
    user,
    queryset: QuerySet,
    *,
    relation_field: str = "user",
    include_department_scope: bool = True,
    include_self: bool = True,
) -> QuerySet:
    """
    Restrict a queryset to rows the current user is allowed to view.

    Parameters
    ----------
    user : apps.accounts.models.User
        The active user requesting the data.
    queryset : QuerySet
        Queryset to scope. Must relate to a user via ``relation_field``.
    relation_field : str, optional
        Name of the relation pointing to a User (default ``"user"``).
    include_department_scope : bool, optional
        When True managers can see department peers (default True).
    include_self : bool, optional
        Include current user's own records (default True).
    """

    if RoleManager.is_admin(user):
        return queryset

    filters = Q()
    if include_self:
        filters |= Q(**{relation_field: user})

    if RoleManager.is_manager(user):
        filters |= Q(**{f"{relation_field}__supervisor": user})
        if include_department_scope and getattr(user, "department_id", None):
            filters |= Q(**{f"{relation_field}__department_id": user.department_id})

    if not filters:
        # Employees without additional privileges can only see themselves.
        filters = Q(**{relation_field: user})

    return queryset.filter(filters).distinct()


def user_has_row_access(viewer, target_user) -> bool:
    """
    Check whether ``viewer`` can access ``target_user``'s resources.
    """
    if viewer == target_user:
        return True
    if RoleManager.is_admin(viewer):
        return True
    if RoleManager.is_manager(viewer):
        if target_user.supervisor_id == viewer.id:
            return True
        if getattr(viewer, "department_id", None) and viewer.department_id == getattr(
            target_user, "department_id", None
        ):
            return True
    return False


def get_accessible_users(user) -> Iterable:
    """
    Return queryset of users accessible to the current user.
    """
    from apps.accounts.models import User  # Local import to avoid circular dependency

    if RoleManager.is_admin(user):
        return User.objects.filter(is_active=True)

    q = Q(pk=user.pk)
    if RoleManager.is_manager(user):
        q |= Q(supervisor=user)
        if getattr(user, "department_id", None):
            q |= Q(department_id=user.department_id)

    return User.objects.filter(q, is_active=True).distinct()


class IsSuperAdminOrAdmin(BasePermission):
    """
    DRF permission allowing access to admins and superadmins.
    """

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        return bool(user and user.is_authenticated and RoleManager.is_admin(user))

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsOwnerOrAdmin(BasePermission):
    """
    Allow access to object owners or administrators.
    """

    def has_permission(self, request, view):
        return bool(getattr(request, "user", None) and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if RoleManager.is_admin(user):
            return True

        target = getattr(obj, "user", None) or getattr(obj, "owner", None) or obj
        return target == user
