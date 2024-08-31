from itertools import chain

from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from vacancies.models import MusicianVacancy, BandVacancy, OrganizerVacancy
from vacancies.serializers import MusicianVacancySerializer, BandVacancySerializer, OrganizerVacancySerializer, \
    VacanciesBaseSerializer
from vacancies.services import create_vacancy
from vacancies.utils import StandartVacancyPagination
from django.core.cache import cache


class VacancyViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    serializer_class = VacanciesBaseSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            match self.request.query_params.get('q'):
                case 'musicians':
                    return MusicianVacancy.objects.all()
                case 'bands':
                    return BandVacancy.objects.all()
                case 'organizers':
                    return OrganizerVacancy.objects.all()
                case _:
                    vacancies_cache = cache.get('vacancies_cache')
                    if vacancies_cache is not None:
                        return vacancies_cache
                    vacancies = list(chain(MusicianVacancy.objects.all(),
                                           BandVacancy.objects.all(),
                                           OrganizerVacancy.objects.all()))
                    cache.set('vacancies_cache', vacancies, 60 * 60)
                    return vacancies

    def get_object(self):
        uuid = self.kwargs.get('uuid')
        vacancies_qs = self.get_queryset()
        for vacancy_obj in vacancies_qs:
            if str(vacancy_obj.uuid) == uuid:
                return vacancy_obj

    def create(self, request, *args, **kwargs):
        vacancy_data = request.data
        if 'type' in vacancy_data:
            match vacancy_data['type']:
                case 'musician':
                    return create_vacancy(MusicianVacancySerializer, vacancy_data)
                case 'band':
                    return create_vacancy(BandVacancySerializer, vacancy_data)
                case 'organizer':
                    return create_vacancy(OrganizerVacancySerializer, vacancy_data)
