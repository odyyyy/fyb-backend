from rest_framework.permissions import BasePermission

from bands.models import Band
from vacancies.models import MusicianVacancy, OrganizerVacancy
from django.shortcuts import get_object_or_404


class AuthorPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, MusicianVacancy) or isinstance(obj, OrganizerVacancy):
            return obj.created_by == request.user
        return obj.leader == request.user
