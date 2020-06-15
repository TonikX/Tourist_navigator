from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
from Tourist_app.models import User


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if(request.user.role == 'student'):
            return True


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if(request.user.role == 'teacher'):
            return True

class IsAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        if(request.user.role == 'author'):
            return True

class IsOwnerProfileOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        print('request.user', request.user)
        #print('obj.user', obj.user)
        print('request.user', request.user)

        return obj == request.user
