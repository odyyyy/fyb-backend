from itertools import chain

from django.http import Http404
from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from bands.models import Band
from users.permissions import AuthorPermission
from users.serializers import UserProfileSerializer
from vacancies.models import MusicianVacancy, BandVacancy, OrganizerVacancy
from vacancies.serializers import VacanciesBaseSerializer


class UsersVacancyView(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = VacanciesBaseSerializer
    permission_classes = [IsAuthenticated, AuthorPermission]
    lookup_field = 'uuid'

    def get_queryset(self):
        user = self.request.user

        musician_vacancies = MusicianVacancy.objects.filter(created_by=user)
        organizer_vacancies = OrganizerVacancy.objects.filter(created_by=user)

        try:
            band = Band.objects.get(leader=user)
            band_vacancies = BandVacancy.objects.filter(created_by=band)
        except Band.DoesNotExist:
            band_vacancies = BandVacancy.objects.none()

        return chain(musician_vacancies, organizer_vacancies, band_vacancies)

    def get_object(self):
        uuid = self.kwargs.get('uuid')
        for obj in self.get_queryset():
            if str(obj.uuid) == uuid:
                return obj

        raise Http404("Object with this UUID does not exist")


class UserFavouritesView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = VacanciesBaseSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return list(chain(MusicianVacancy.objects.filter(favourites=user),
                          BandVacancy.objects.filter(favourites=user),
                          OrganizerVacancy.objects.filter(favourites=user)))

    def create(self, request, *args, **kwargs):
        uuid = request.data.get('uuid')
        vacancy = MusicianVacancy.objects.filter(uuid=uuid).union(
            BandVacancy.objects.filter(uuid=uuid),
            OrganizerVacancy.objects.filter(uuid=uuid))

        if len(vacancy) != 0:
            vacancy[0].favourites.add(request.user)

    def destroy(self, request, *args, **kwargs):
        uuid = self.kwargs.get('uuid')
        vacancy = MusicianVacancy.objects.filter(uuid=uuid).union(
            BandVacancy.objects.filter(uuid=uuid),
            OrganizerVacancy.objects.filter(uuid=uuid))

        if len(vacancy) != 0:
            vacancy[0].favourites.remove(request.user)


class UserProfileView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


def auth(request):
    return render(request, 'oauth.html')
