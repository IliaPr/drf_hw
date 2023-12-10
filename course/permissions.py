from rest_framework import permissions


class IsModeratorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Проверяем, принадлежит ли пользователь группе "Модераторы"
        return request.user.groups.filter(name='Модераторы').exists()

    def has_object_permission(self, request, view, obj):
        # Разрешаем только чтение и изменение объектов
        if request.method in permissions.SAFE_METHODS:
            return True
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
