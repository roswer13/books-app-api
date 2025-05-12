"""
Permissions for the book and page APIs.
"""
from rest_framework import permissions

from core.constants.roles_enum import Roles


class IsEditorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow editors to edit books and pages.
    Readers can only view.
    """
    def has_permission(self, request, view):
        # Require authentication for any access
        if not request.user or not request.user.is_authenticated:
            return False
        # Allow safe methods (GET, HEAD, OPTIONS) for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow non-safe methods only to editors
        return request.user.role == Roles.EDITOR
