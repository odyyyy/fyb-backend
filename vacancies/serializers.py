from rest_framework import serializers

from vacancies.models import MusicianVacancy, BandVacancy, OrganizerVacancy

from rest_framework import serializers
from .models import MusicianVacancy, BandVacancy, OrganizerVacancy


class FavoriteVacancySerializer(serializers.Serializer):


    def to_representation(self, vacancy_obj):
        return choose_vacancy_serializer(vacancy_obj)


class VacanciesBaseSerializer(serializers.Serializer):

    def to_representation(self, vacancy_obj):
        return choose_vacancy_serializer(vacancy_obj)


class MusicianVacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicianVacancy
        fields = '__all__'



class BandVacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = BandVacancy
        fields = '__all__'


class OrganizerVacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizerVacancy
        fields = '__all__'


def choose_vacancy_serializer(vacancy_obj):
    if isinstance(vacancy_obj, MusicianVacancy):
        return MusicianVacancySerializer(vacancy_obj).data
    elif isinstance(vacancy_obj, BandVacancy):
        return BandVacancySerializer(vacancy_obj).data
    elif isinstance(vacancy_obj, OrganizerVacancy):
        return OrganizerVacancySerializer(vacancy_obj).data
