from rest_framework import permissions
from .models import Tutor


class UpdateOwnPet(permissions.BasePermission):
    def is_owner(self, request, view, obj):
        tutor = Tutor.objects.get(user=request.user)
        return tutor.id == obj.tutor.id
