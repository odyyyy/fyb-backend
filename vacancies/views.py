from django.utils.translation import gettext as _
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from vacancies.serializers import VacanciesBaseSerializer
from vacancies.services import create_periodic_adding_vacancies_task, \
    get_vacancies_queryset_by_query_type


class VacancyViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    serializer_class = VacanciesBaseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        query_type = self.request.query_params.get('q')
        return get_vacancies_queryset_by_query_type(query_type)

    def get_object(self):
        uuid = self.kwargs.get('uuid')
        vacancies_qs = self.get_queryset()
        for vacancy_obj in vacancies_qs:
            if str(vacancy_obj.uuid) == uuid:
                return vacancy_obj

    def create(self, request, *args, **kwargs):
        vacancy_data = request.data

        # Отложенное создание объявления если задано поле даты
        if 'date' in vacancy_data:
            create_periodic_adding_vacancies_task(vacancy_data)
            return Response({'detail': _('Periodic task was created successfully')}, status=201)

        return super().create(request, *args, **kwargs)

