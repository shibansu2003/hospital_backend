from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerForPatients(BasePermission):
    """
    - For Patient objects: only the creator can retrieve/update/delete.
    - List is auto-filtered in the view; this guard is for object-level safety.
    """
    def has_object_permission(self, request, view, obj):
        return getattr(obj, "created_by_id", None) == request.user.id


class IsAuthenticatedOrReadDoctors(BasePermission):
    """
    - Allow read access to doctors for anyone.
    - Write operations require authentication.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
