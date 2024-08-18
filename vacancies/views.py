from django.db.models import QuerySet
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, RetrieveAPIView

from vacancies.models import MusicianVacancy, BandVacancy, OrganizerVacancy
from vacancies.serializers import MusicianVacancySerializer, BandVacancySerializer, OrganizerVacancySerializer, \
    VacanciesUniversalSerializer
from itertools import chain


class VacancyListView(ListAPIView):
    serializer_class = VacanciesUniversalSerializer

    def get_queryset(self):
        match self.request.query_params.get('q'):
            case 'musicians':
                return MusicianVacancy.objects.all()
            case 'bands':
                return BandVacancy.objects.all()
            case 'organizers':
                return OrganizerVacancy.objects.all()
            case _:
                return list(chain(MusicianVacancy.objects.all(),
                                  BandVacancy.objects.all(),
                                  OrganizerVacancy.objects.all()))


class VacancyItemView(RetrieveAPIView):
    serializer_class = VacanciesUniversalSerializer
    lookup_field = 'uuid'

    def get_object(self):
        uuid = self.kwargs.get('uuid')
        try:
            return MusicianVacancy.objects.get(uuid=uuid)
        except MusicianVacancy.DoesNotExist:
            try:
                return BandVacancy.objects.get(uuid=uuid)
            except BandVacancy.DoesNotExist:
                try:
                    return OrganizerVacancy.objects.get(uuid=uuid)
                except OrganizerVacancy.DoesNotExist:
                    raise NotFound("No vacancy matches the given uuid.")