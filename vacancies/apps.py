from django.apps import AppConfig


class VacanciesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vacancies'
    verbose_name = "Объявления"


    def ready(self):
        import vacancies.signals