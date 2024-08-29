""" This File will hold permissions for app """

from rest_framework.permissions import BasePermission

class IsReviewOwner(BasePermission):
    """ Permission class for ownership of the review. """
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.reviewer == request.user
        return True
