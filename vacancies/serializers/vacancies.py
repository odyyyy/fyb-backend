import re

from rest_framework import serializers

from vacancies.models import MusicianVacancy, BandVacancy, OrganizerVacancy
from vacancies.serializers.mixins import VacancyWithDateTimeMixin, VacancyContactsValidatorMixin


class MusicianVacancyDetailSerializer(VacancyWithDateTimeMixin, VacancyContactsValidatorMixin,
                                      serializers.ModelSerializer):
    class Meta:
        model = MusicianVacancy
        fields = '__all__'


class MusicianVacancyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicianVacancy
        fields = ('uuid', 'created_by', 'created_at', 'city', 'instruments', 'level', 'favourites')


class BandVacancyDetailSerializer(VacancyWithDateTimeMixin, VacancyContactsValidatorMixin, serializers.ModelSerializer):
    class Meta:
        model = BandVacancy
        fields = '__all__'


class BandVacancyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BandVacancy
        fields = ('uuid', 'created_by', 'created_at', 'city', 'instrument', 'favourites')


class OrganizerVacancyDetailSerializer(VacancyWithDateTimeMixin, VacancyContactsValidatorMixin,
                                       serializers.ModelSerializer):
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

    def validate_address(self, value):
        address_pattern = r'^[A-Za-zА-Яа-яЁё\s]+,\s*[A-Za-zА-Яа-яЁё\s]+,\s*\d+$'
        if not re.match(address_pattern, value):
            raise serializers.ValidationError("Адрес должен быть в формате 'Город, Улица, Номер дома'.")
        return value


class FavoriteVacancySerializer(serializers.Serializer):

    def to_representation(self, vacancy_obj):
        return choose_vacancy_serializer(vacancy_obj)


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
