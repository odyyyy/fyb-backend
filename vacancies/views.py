import logging

from django.utils.translation import gettext as _
from rest_framework import mixins
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from vacancies.serializers import VacanciesBaseSerializer
from vacancies.services import create_periodic_adding_vacancies_task, \
    get_vacancies_queryset_by_query_params

logger = logging.getLogger(__name__)


class VacancyViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    serializer_class = VacanciesBaseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    lookup_field = 'uuid'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['view_action'] = self.action
        return context

    def get_queryset(self):
        query_params = self.request.query_params
        return get_vacancies_queryset_by_query_params(query_params)

    def get_object(self):
        uuid = self.kwargs.get('uuid')

        vacancies_qs = self.get_queryset()
        for vacancy_obj in vacancies_qs:
            if str(vacancy_obj.uuid) == uuid:
                return vacancy_obj
        raise NotFound(detail=_('Vacancy not found'), code=404)

    def create(self, request, *args, **kwargs):
        vacancy_data = request.data

        # Отложенное создание объявления если задано поле даты
        if 'date' in vacancy_data:
            logger.debug(f'Create new vacancy at time specified by user {vacancy_data.get("uuid")}')
            logger.info('Executing create_vacancy_at_time_chosen_by_user task')

            create_periodic_adding_vacancies_task(vacancy_data)

            return Response({'detail': _('Periodic task was created successfully')}, status=201)

        return super().create(request, *args, **kwargs)
