from rest_framework.permissions import BasePermission

from bands.models import Band


class BandLeaderPermission(BasePermission):
    def has_permission(self, request, view):
        return Band.objects.filter(leader=request.user).exists() or request.method == 'POST'