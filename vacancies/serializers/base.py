from rest_framework import serializers

from vacancies.serializers.vacancies import choose_vacancy_serializer, MusicianVacancyDetailSerializer, \
    BandVacancyDetailSerializer, OrganizerVacancyDetailSerializer


class VacanciesBaseSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.view_action = self.context.get('view_action', None)

    def to_representation(self, vacancy_obj):
        return choose_vacancy_serializer(vacancy_obj, self.view_action)

    def run_validation(self, data):
        """ Не выполняем валидацию для полей т.к.
         сериализатор выполняет роль посредника """
        return data

    def create(self, validated_data):
        vacancy_type = validated_data.pop('type', None)

        if vacancy_type == 'musician':
            serializer = MusicianVacancyDetailSerializer(data=validated_data)
        elif vacancy_type == 'band':
            serializer = BandVacancyDetailSerializer(data=validated_data)
        elif vacancy_type == 'organizer':
            serializer = OrganizerVacancyDetailSerializer(data=validated_data)
        else:
            raise serializers.ValidationError('Unknown vacancy type')

        if serializer.is_valid(raise_exception=True):
            return serializer.save()
        raise serializers.ValidationError('Invalid data for the vacancy type')
