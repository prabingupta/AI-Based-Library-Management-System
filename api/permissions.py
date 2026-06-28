from rest_framework.permissions import BasePermission


class IsLibraryAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["super_admin", "library_admin"]


class IsLibrarianOrAbove(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            "super_admin",
            "library_admin",
            "librarian",
            "assistant_librarian",
        ]


class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return request.user.role in ["super_admin", "library_admin", "librarian", "assistant_librarian"]
