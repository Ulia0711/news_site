from rest_framework import permissions
from .models import User

class SuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == User.SUPERADMIN
        return False
    
class News_editor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == User.NEWS_EDITOR
        return False
    
class Reader(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == User.READER
        return False