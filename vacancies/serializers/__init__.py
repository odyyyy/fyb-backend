from .vacancies import (MusicianVacancyDetailSerializer,
                        MusicianVacancyListSerializer,
                        BandVacancyDetailSerializer,
                        BandVacancyListSerializer,
                        OrganizerVacancyDetailSerializer,
                        OrganizerVacancyListSerializer,
                        FavoriteVacancySerializer)
from .base import VacanciesBaseSerializer

__all__ = [
    'MusicianVacancyListSerializer',
    'MusicianVacancyDetailSerializer',
    'BandVacancyListSerializer',
    'BandVacancyDetailSerializer',
    'OrganizerVacancyListSerializer',
    'OrganizerVacancyDetailSerializer',
    'FavoriteVacancySerializer',
    'VacanciesBaseSerializer',
]
