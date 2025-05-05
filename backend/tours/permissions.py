from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_permission(self, request, view):
        # Allow all GET, HEAD, OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow authenticated users for POST, PUT, PATCH, DELETE
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Allow all GET, HEAD, OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow tour author to edit/delete
        return obj.author == request.user 