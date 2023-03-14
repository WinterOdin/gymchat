from rest_framework import permissions

class GymLocationPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == ['list', 'create', 'retrieve']:
            return request.user.is_authenticated 
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user.is_staff
        else:
            return False
                                                                                                
    def has_object_permission(self, request, view, obj):
        
        if not request.user.is_authenticated:
            return False

        if view.action in ['update', 'partial_update',]:
            return obj == request.user or request.user.is_staff
        elif view.action == 'destroy':
            return request.user.is_staff
        else:
            return False