from rest_framework import permissions


class IsAuthorModerAdminOrReadOnly(permissions.BasePermission):
    '''Доступ для отзывов и комментариев. Чтение любой пользователь.
       Остальные методы: автор, модератор или админ'''
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return (
                obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin
            )
        return True


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser)))
