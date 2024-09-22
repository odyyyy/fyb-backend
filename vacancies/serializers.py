from rest_framework import serializers

from .models import MusicianVacancy, BandVacancy, OrganizerVacancy


class VacancyWithDateTimeMixin:
    date = serializers.DateTimeField(write_only=True)


class FavoriteVacancySerializer(serializers.Serializer):

    def to_representation(self, vacancy_obj):
        return choose_vacancy_serializer(vacancy_obj)


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


class MusicianVacancyDetailSerializer(VacancyWithDateTimeMixin, serializers.ModelSerializer):
    class Meta:
        model = MusicianVacancy
        fields = '__all__'


class MusicianVacancyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicianVacancy
        fields = ('uuid', 'created_by', 'created_at', 'city', 'instruments', 'level', 'favourites')


class BandVacancyDetailSerializer(VacancyWithDateTimeMixin, serializers.ModelSerializer):
    class Meta:
        model = BandVacancy
        fields = '__all__'


class BandVacancyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BandVacancy
        fields = ('uuid', 'created_by', 'created_at', 'city', 'instrument', 'favourites')


class OrganizerVacancyDetailSerializer(VacancyWithDateTimeMixin, serializers.ModelSerializer):
    class Meta:
        model = OrganizerVacancy
        fields = '__all__'


class OrganizerVacancyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizerVacancy
        fields = ('uuid', 'title', 'created_by', 'created_at', 'address', 'event_datetime', 'favourites')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['address'] = data['address'].split(',')[0]
        return data


def choose_vacancy_serializer(vacancy_obj, view_action):
    if isinstance(vacancy_obj, MusicianVacancy):
        return MusicianVacancyListSerializer(vacancy_obj).data if view_action == 'list' \
            else MusicianVacancyDetailSerializer(vacancy_obj).data
    elif isinstance(vacancy_obj, BandVacancy):
        return BandVacancyListSerializer(vacancy_obj).data if view_action == 'list' \
            else BandVacancyDetailSerializer(vacancy_obj).data
    elif isinstance(vacancy_obj, OrganizerVacancy):
        return OrganizerVacancyListSerializer(vacancy_obj).data if view_action == 'list' \
            else OrganizerVacancyDetailSerializer(vacancy_obj).data
    raise serializers.ValidationError('Unknown vacancy object type')
