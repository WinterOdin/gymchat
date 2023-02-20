from rest_framework import permissions

class ProfilePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated 
        elif view.action == 'create':
            return True
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
                                                                                                
    def has_object_permission(self, request, view, obj):
        
        if not request.user.is_authenticated:
            return False

        if view.action == 'retrieve':
            return obj == request.user or request.user.is_staff
        elif view.action in ['update', 'partial_update']:
            return obj == request.user or request.user.is_staff
        elif view.action == 'destroy':
            return request.user.is_staff
        else:
            return False

class DisplayMatchesPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if view.action in ['list', 'retrive']:
            return request.user.is_authenticated 
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return False
        else:
            return False
                                                                                                
    def has_object_permission(self, request, view, obj):
        
        if not request.user.is_authenticated:
            return False

        if view.action == 'retrieve':
            return obj == request.user or request.user.is_staff
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user.is_staff
        else:
            return False