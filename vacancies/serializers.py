from rest_framework import serializers

from vacancies.models import MusicianVacancy, BandVacancy, OrganizerVacancy

from rest_framework import serializers
from .models import MusicianVacancy, BandVacancy, OrganizerVacancy


class FavoriteVacancySerializer(serializers.Serializer):

    def to_representation(self, obj):
        context = self.context.copy()
        context['parent_serializer'] = FavoriteVacancySerializer

        if isinstance(obj, MusicianVacancy):
            return MusicianVacancySerializer(obj, context=context).data
        elif isinstance(obj, BandVacancy):
            return BandVacancySerializer(obj, context=context).data
        elif isinstance(obj, OrganizerVacancy):
            return OrganizerVacancySerializer(obj, context=context).data

        return super().to_representation(obj)


class VacanciesBaseSerializer(serializers.Serializer):

    def to_representation(self, obj):
        if isinstance(obj, MusicianVacancy):
            return MusicianVacancySerializer(obj).data
        elif isinstance(obj, BandVacancy):
            return BandVacancySerializer(obj).data
        elif isinstance(obj, OrganizerVacancy):
            return OrganizerVacancySerializer(obj).data
        return super().to_representation(obj)


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
