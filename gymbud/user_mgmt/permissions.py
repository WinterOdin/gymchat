from rest_framework import permissions

class ProfilePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return request.user.is_authenticated 
        else:
            return False
                                                                                                
    def has_object_permission(self, request, view, obj):
        
        if not request.user.is_authenticated:
            return False

        if view.action in ['update', 'partial_update', 'retrieve', 'destroy']:
            return obj == request.user or request.user.is_staff
        else:
            return False

