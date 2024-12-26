from django.db.models import signals
from notifications.tasks import send_new_vacancy_notification
from vacancies.models import OrganizerVacancy, MusicianVacancy, BandVacancy


@signals.post_save.connect
def on_vacancy_save_send_notification(sender, instance, created, **kwargs):
    print(sender, instance, created, kwargs)
    if sender in (OrganizerVacancy, MusicianVacancy, BandVacancy):
        if created:
            send_new_vacancy_notification.delay(sender.__name__)
