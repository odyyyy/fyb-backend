import json
from itertools import chain

from django_celery_beat.models import PeriodicTask, ClockedSchedule
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from vacancies.models import MusicianVacancy, BandVacancy, OrganizerVacancy


def create_vacancy(serializer_class: Serializer, vacancy_data: dict) -> Response:
    serializer = serializer_class(data=vacancy_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)


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


def get_vacancies_queryset_by_query_type(query_type: str):
    match query_type:
        case 'musicians':
            return MusicianVacancy.objects.with_related()
        case 'bands':
            return BandVacancy.objects.with_related()
        case 'organizers':
            return OrganizerVacancy.objects.with_related()
        case _:
            return chain(MusicianVacancy.objects.with_related(),
                         BandVacancy.objects.with_related(),
                         OrganizerVacancy.objects.with_related())
