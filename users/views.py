from itertools import chain

from rest_framework import generics, mixins
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from vacancies.models import MusicianVacancy, BandVacancy, OrganizerVacancy
from vacancies.serializers import VacanciesUniversalSerializer


class UserFavouritesListView(ListAPIView):
    serializer_class = VacanciesUniversalSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return chain(MusicianVacancy.objects.filter(favourites=user),
                     BandVacancy.objects.filter(favourites=user),
                     OrganizerVacancy.objects.filter(favourites=user))

class UserFavouriteDestroyView(mixins.DestroyModelMixin,
                               mixins.CreateModelMixin,
                               generics.GenericAPIView):
    def create(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')

