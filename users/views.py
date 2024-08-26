from itertools import chain
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from vacancies.models import MusicianVacancy, BandVacancy, OrganizerVacancy
from vacancies.serializers import VacanciesBaseSerializer


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






# class UserFavouriteCreateDestroyView(mixins.DestroyModelMixin,
#                                mixins.CreateModelMixin,
#                                generics.GenericAPIView):
#
#     permission_classes = [IsAuthenticated, ]
#
#     def create(self, request, *args, **kwargs):
#         uuid = kwargs.get('uuid')
#         musician_vacancy = MusicianVacancy.objects.filter(uuid=uuid)
#         if musician_vacancy.exists() and not (musician_vacancy.favourites.filter(id=request.user.id).exists()):
#             musician_vacancy.first().favourites.add(request.user)
#
#         elif BandVacancy.objects.filter(uuid=uuid).exists() and not (BandVacancy.objects.filter(uuid=uuid).favourites.filter(id=request.user.id).exists()):
#             BandVacancy.objects.filter(uuid=uuid).first().favourites.add(request.user)
#
#         elif OrganizerVacancy.objects.filter(uuid=uuid).exists() and not (OrganizerVacancy.objects.filter(uuid=uuid).favourites.filter(id=request.user.id).exists()):
#             OrganizerVacancy.objects.filter(uuid=uuid).first().favourites.add(request.user)
#
#
#         return self.create(request, *args, **kwargs)
#
#     def destroy(self, request, *args, **kwargs):
#         uuid = kwargs.get('uuid')
#         musician_vacancy = MusicianVacancy.objects.filter(uuid=uuid)
#         if musician_vacancy.exists() and musician_vacancy.favourites.filter(id=request.user.id).exists():
#             musician_vacancy.first().favourites.remove(request.user)
#
#         elif BandVacancy.objects.filter(uuid=uuid).exists() and BandVacancy.objects.filter(uuid=uuid).favourites.filter(id=request.user.id).exists():
#             BandVacancy.objects.filter(uuid=uuid).first().favourites.remove(request.user)
#
#         elif OrganizerVacancy.objects.filter(uuid=uuid).exists() and OrganizerVacancy.objects.filter(uuid=uuid).favourites.filter(id=request.user.id).exists():
#             OrganizerVacancy.objects.filter(uuid=uuid).first().favourites.remove(request.user)
#
#         return self.destroy(request, *args, **kwargs)
