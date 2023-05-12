from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        is_admin = request.user.is_staff or request.user.is_superuser
        return request.method in SAFE_METHODS or is_admin


class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        is_staff = request.user.is_staff
        is_super = request.user.is_superuser
        return is_super or is_staff


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_owner = obj.account == request.user
        is_staff = request.user.is_staff or request.user.is_superuser
        is_owner = is_owner or is_staff
        return is_owner or request.method in SAFE_METHODS
