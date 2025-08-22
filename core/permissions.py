from rest_framework.permissions import BasePermission


def has_permission_code(user, code):
    """Helper: check if user has a specific permission code."""
    if not user or not user.is_authenticated:
        return False
    if not user.role:
        return False
    return user.role.permissions.filter(code=code).exists()


class IsAdminPermission(BasePermission):
    """Allow if user has 'manage_roles' permission (admin)."""

    def has_permission(self, request, view):
        return has_permission_code(request.user, "manage_roles")


class CanManageUsers(BasePermission):
    """Allow if user has user create/update/delete/list permission."""

    def has_permission(self, request, view):
        return (
            has_permission_code(request.user, "create_user")
            or has_permission_code(request.user, "update_user")
            or has_permission_code(request.user, "delete_user")
            or has_permission_code(request.user, "view_all_users")
        )


class CanViewEmployeesOnly(BasePermission):
    """Allow if user has 'view_employees_only' permission."""

    def has_permission(self, request, view):
        return has_permission_code(request.user, "view_employees_only")


class IsSelfOrAdmin(BasePermission):
    """Allow if user is self OR has manage_roles permission (admin)."""

    def has_object_permission(self, request, view, obj):
        if has_permission_code(request.user, "manage_roles"):
            return True
        return obj.id == request.user.id
