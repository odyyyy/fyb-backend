import logging

from celery import shared_task

from vacancies.serializers import VacanciesBaseSerializer

logger = logging.getLogger(__name__)


@shared_task
def create_vacancy_at_time_chosen_by_user(vacancy_data: dict):
    logger.info("Running create_vacancy_at_time_chosen_by_user task")
    logger.debug(f'Create new vacancy at time specified by user {vacancy_data.get("uuid")}')

    serializer = VacanciesBaseSerializer(data=vacancy_data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        logger.debug(f'Vacancy created successfully {serializer.data}')

    else:
        logger.error(f'Validation errors: {serializer.errors}')
