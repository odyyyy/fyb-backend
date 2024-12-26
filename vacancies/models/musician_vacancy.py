from django.contrib.postgres.fields import ArrayField
from django.db import models

from vacancies.models.base import BaseMusicVacancy, INSTRUMENTS


class MusicianVacancy(BaseMusicVacancy):
    instruments = ArrayField(
        models.CharField(max_length=50, choices=INSTRUMENTS),
        size=3,
        default=list,
        verbose_name="Инструменты"
    )

    class Meta:
        verbose_name = "Объявление музыканта"
        verbose_name_plural = "Объявления музыкантов"
