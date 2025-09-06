from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerForPatients(BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(obj, "created_by_id", None) == request.user.id


class IsAuthenticatedOrReadDoctors(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
