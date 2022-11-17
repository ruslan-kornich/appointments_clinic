from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_superuser and request.user.is_staff:
            return True

    def has_object_permission(self, request, view, obj):
        if (request.user.is_superuser and
                request.user.is_staff and
                request.user.is_admin):
            return True
        return False


class IsManager(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return False


class IsClient(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return False


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
