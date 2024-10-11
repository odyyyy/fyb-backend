import json
import re
from datetime import datetime
from itertools import chain
from typing import Any, Union

from django.http import QueryDict
from django_celery_beat.models import PeriodicTask, ClockedSchedule

from vacancies.models import MusicianVacancy, BandVacancy, OrganizerVacancy


def get_vacancies_queryset_by_query_params(query_params: QueryDict[str, Any]):
    query_params = dict(query_params)

    filter_params = get_prepared_filter_params(query_params)
    vacancy_type = filter_params.pop('type', None)

    match vacancy_type:
        case 'musicians':
            return MusicianVacancy.objects.with_related().filter(**filter_params)
        case 'bands':
            return BandVacancy.objects.with_related().filter(**filter_params)
        case 'organizers':
            return OrganizerVacancy.objects.with_related().filter(**filter_params)
        case _:
            return chain(MusicianVacancy.objects.with_related().filter(**filter_params),
                         BandVacancy.objects.with_related().filter(**filter_params),
                         OrganizerVacancy.objects.with_related().filter(**filter_params))


def get_prepared_filter_params(query_params: dict[str, Any]) -> dict[str, Any]:
    filter_fields = {
        'created_by': int,
        'created_at': datetime,
        'type': str
    }
    music_vacancy_filter_fields = {
        'genres': str,
        'instrument': str,
        'instruments': list,
        'city': str,
        'level': str
    }

    organizer_vacancy_filter_fields = {
        'event_type': str,
        'address': str,
        'event_datetime': datetime
    }

    query_params = get_unpacked_query_params(query_params)

    vacancy_type = query_params.get('type', None)

    if vacancy_type in ('musicians', 'bands'):
        validated_filter_fields = validate_filters_params(query_params, filter_fields | music_vacancy_filter_fields)
    elif vacancy_type == 'organizers':
        validated_filter_fields = validate_filters_params(query_params, filter_fields | organizer_vacancy_filter_fields)
    else:
        validated_filter_fields = validate_filters_params(query_params, filter_fields)

    return validated_filter_fields


def validate_filters_params(query_params: dict[str, Any], allowed_fields: dict[str, Any]):
    for field in query_params.copy().keys():
        if (field not in allowed_fields or not (
                is_able_to_cast_value_to_type(query_params[field], allowed_fields[field])) or
                is_incorrect_list_query_params_format(allowed_fields[field], query_params[field])):
            query_params.pop(field)

    return query_params


def is_able_to_cast_value_to_type(value: str, type_: type) -> bool:
    try:
        if isinstance(value, list):
            type_(value[0])
        else:
            type_(value)
        return True
    except ValueError | IndexError:
        return False


def is_incorrect_list_query_params_format(query_param_type: Union[int, str, list], query_list_param: str) -> bool:
    return (query_param_type is list and (re.findall('{.*[^,]}$', query_list_param) == []
                                          or (query_list_param.count('{') != 1 or query_list_param.count('}') != 1)))


def get_unpacked_query_params(query_params: dict[str, Any]) -> dict[str, Any]:
    query_params = query_params.copy()
    for param, value in query_params.items():
        if isinstance(value, list) and len(value) == 1:
            query_params[param] = value[0]

    return query_params


def create_periodic_adding_vacancies_task(vacancy_data: dict):
    run_at: str = vacancy_data.get('date')
    schedule, created = ClockedSchedule.objects.get_or_create(
        clocked_time=run_at
    )

    del vacancy_data['date']

    PeriodicTask.objects.create(
        name=f'Create vacancy at time specified by user {vacancy_data.get("uuid")}',
        task='vacancies.tasks.create_vacancy_at_time_chosen_by_user',
        clocked=schedule,
        kwargs=json.dumps({'vacancy_data': vacancy_data}),
        one_off=True,
    )
