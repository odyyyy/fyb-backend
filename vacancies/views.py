from django.db.models import QuerySet
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from vacancies.models import MusicianVacancy, BandVacancy, OrganizerVacancy
from vacancies.serializers import MusicianVacancySerializer, BandVacancySerializer, OrganizerVacancySerializer, \
    VacanciesBaseSerializer
from itertools import chain



class VacancyViewSet(ModelViewSet):
    serializer_class = VacanciesBaseSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'uuid'

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

    def create(self, request, *args, **kwargs):
        vacancy_data = request.data

        if 'type' in vacancy_data:
            match vacancy_data['type']:
                case 'musician':
                    return self.create_vacancy(MusicianVacancySerializer, vacancy_data)
                case 'band':
                    return self.create_vacancy(BandVacancySerializer, vacancy_data)
                case 'organizer':
                    return self.create_vacancy(OrganizerVacancySerializer, vacancy_data)

    def create_vacancy(self, serializer_class, vacancy_data):
        serializer = serializer_class(data=vacancy_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

