from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return user.groups.filter(name__in=("Manager", "Admin")).exists()

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.groups.filter(name__in=("Manager", "Admin")).exists():
            return True

        if request.method in SAFE_METHODS:
            return obj.assigned_to == user

        return False
