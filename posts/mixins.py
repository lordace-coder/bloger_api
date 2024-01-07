from rest_framework.permissions import (DjangoModelPermissions, IsAdminUser,
                                        IsAuthenticatedOrReadOnly)


class StaffEditorPermission(DjangoModelPermissions):
    def has_permission(self, request, view):
        user = request.user
        if user.is_staff:
            return True
        return False




class StaffEditOnly:
    permission_classes = [IsAdminUser,StaffEditorPermission]

class UserEditOnly:
    permission_classes = [IsAuthenticatedOrReadOnly]