import logging

from celery import shared_task

from vacancies.serializers import VacanciesBaseSerializer

logger = logging.getLogger(__name__)

@shared_task
def create_vacancy_at_time_chosen_by_user(vacancy_data: dict):
    logger.info('Executing create_vacancy_at_time_chosen_by_user task')
    logger.debug(f'Vacancy data {vacancy_data}')
    serializer = VacanciesBaseSerializer(data=vacancy_data)

    if serializer.is_valid(raise_exception=True):
        # WARNING: serializer.data is None
        serializer.save()
        logger.info('Vacancy was created successfully')
    else:
        logger.error(f'Validation errors: {serializer.errors}')
