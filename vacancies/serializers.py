from rest_framework import serializers

from .models import MusicianVacancy, BandVacancy, OrganizerVacancy


class VacancyWithDateTimeMixin:
    date = serializers.DateTimeField(write_only=True)


class FavoriteVacancySerializer(serializers.Serializer):

    def to_representation(self, vacancy_obj):
        return choose_vacancy_serializer(vacancy_obj)


class VacanciesBaseSerializer(serializers.Serializer):
    type = serializers.CharField(write_only=True)

    def to_representation(self, vacancy_obj):
        return choose_vacancy_serializer(vacancy_obj)

    def run_validation(self, data):
        """ Не выполняем валидацию для полей т.к.
         сериализатор выполняет роль посредника """
        return data

    def create(self, validated_data):
        vacancy_type = validated_data.pop('type', None)

        if vacancy_type == 'musician':
            serializer = MusicianVacancySerializer(data=validated_data)
        elif vacancy_type == 'band':
            serializer = BandVacancySerializer(data=validated_data)
        elif vacancy_type == 'organizer':
            serializer = OrganizerVacancySerializer(data=validated_data)
        else:
            raise serializers.ValidationError('Unknown vacancy type')

        if serializer.is_valid(raise_exception=True):
            return serializer.save()
        raise serializers.ValidationError('Invalid data for the vacancy type')


class MusicianVacancySerializer(VacancyWithDateTimeMixin, serializers.ModelSerializer):
    class Meta:
        model = MusicianVacancy
        fields = '__all__'


class BandVacancySerializer(VacancyWithDateTimeMixin, serializers.ModelSerializer):
    class Meta:
        model = BandVacancy
        fields = '__all__'


class OrganizerVacancySerializer(VacancyWithDateTimeMixin, serializers.ModelSerializer):
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
    raise serializers.ValidationError('Unknown vacancy object type')
