#coding=utf-8

from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.role ==3:
                return False
            else:
                return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.role ==3:
                return False
            else:
                return True


class IsSuperAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            if request.user.role ==3:
                return False
            else:
                return True
        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method not in permissions.SAFE_METHODS:
            if request.user.role ==3:
                return False
            elif request.user.role ==2:
                return obj.role > request.user.role
            else:
                return True
        return True

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.role == 3:
            if request.method in permissions.SAFE_METHODS:
                return True
            return obj.user == request.user
        return True

