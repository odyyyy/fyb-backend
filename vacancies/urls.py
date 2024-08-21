from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import VacancyListView, VacancyItemView


urlpatterns = [
    path('', VacancyListView.as_view(), name='vacancies_list'),
    path('<uuid:uuid>/', VacancyItemView.as_view(), name='vacancy_item'),
]
