from celery import shared_task

from vacancies.serializers import VacanciesBaseSerializer


@shared_task
def create_vacancy_at_time_chosen_by_user(vacancy_data: dict):
    serializer = VacanciesBaseSerializer(data=vacancy_data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
    else:
        # add logger
        print('Validation errors:', serializer.errors)
