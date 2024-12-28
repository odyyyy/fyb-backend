from rest_framework.permissions import IsAuthenticatedOrReadOnly


class VacancyCreatorPermission(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.created_by
