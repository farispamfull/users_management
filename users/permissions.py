from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import User


class ReadOnlyPermmissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return (request.user.role == User.is_admin
                or request.user.is_staff
                or request.user.is_superuser)


class IsAdministratorPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
                request.user.role == User.is_admin
                or request.user.is_staff
                or request.user.is_superuser
        )
